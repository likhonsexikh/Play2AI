#!/usr/bin/env python3
"""
Enhanced Play2AI Agent Runtime with MCP Integration
"""
import os
import json
import time
import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
import uvicorn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Play2AIAgent:
    def __init__(self):
        self.ai_model = os.getenv('AI_MODEL', 'llama3')
        self.task_mode = os.getenv('TASK_MODE', 'autonomous')
        self.android_host = os.getenv('ANDROID_EMULATOR_HOST', 'android-emulator')
        self.android_port = os.getenv('ANDROID_EMULATOR_PORT', '5554')
        self.mcp_url = os.getenv('MCP_SERVER_URL', 'http://android-mcp:8081')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.workspace = Path('/workspace')
        self.screenshots_dir = Path('/screenshots')
        self.screenshots_dir.mkdir(exist_ok=True)

        # Initialize AI client based on model
        self.init_ai_client()

        # FastAPI app for external control
        self.app = FastAPI(title="Play2AI Agent", version="2.0")
        self.setup_routes()

    def init_ai_client(self):
        """Initialize AI client based on selected model"""
        if 'gpt' in self.ai_model.lower():
            import openai
            self.ai_client = openai.OpenAI()
        elif 'gemini' in self.ai_model.lower() or 'gemma' in self.ai_model.lower():
            import google.generativeai as genai
            self.ai_client = genai
        else:
            # Default to Anthropic/Claude
            import anthropic
            self.ai_client = anthropic.Anthropic()

    def setup_routes(self):
        """Setup FastAPI routes"""
        @self.app.get("/")
        async def root():
            return {"status": "Play2AI Agent Running", "model": self.ai_model}

        @self.app.post("/execute_task")
        async def execute_task(task: Dict[str, Any], background_tasks: BackgroundTasks):
            background_tasks.add_task(self.execute_autonomous_task, task)
            return {"status": "Task queued", "task": task}

        @self.app.get("/status")
        async def get_status():
            return {
                "agent_status": "active",
                "android_connection": await self.check_android_connection(),
                "mcp_connection": await self.check_mcp_connection(),
                "current_task": getattr(self, 'current_task', None)
            }

    async def check_android_connection(self) -> bool:
        """Check if Android emulator is accessible"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
            return 'emulator' in result.stdout or 'device' in result.stdout
        except Exception as e:
            logger.error(f"Android connection check failed: {e}")
            return False

    async def check_mcp_connection(self) -> bool:
        """Check if MCP server is accessible"""
        try:
            response = requests.get(f"{self.mcp_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"MCP connection check failed: {e}")
            return False

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """Take screenshot of Android emulator"""
        if not filename:
            filename = f"screenshot_{int(time.time())}.png"

        screenshot_path = self.screenshots_dir / filename

        try:
            # Use ADB to take screenshot
            subprocess.run([
                'adb', '-s', f'{self.android_host}:{self.android_port}',
                'exec-out', 'screencap', '-p'
            ], stdout=open(screenshot_path, 'wb'), check=True, timeout=30)

            logger.info(f"Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return ""

    async def query_ai_model(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Query AI model with context"""
        try:
            if hasattr(self.ai_client, 'messages'):  # Anthropic
                response = self.ai_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            else:
                # Generic completion approach
                return f"AI Response for: {prompt[:100]}..."
        except Exception as e:
            logger.error(f"AI query failed: {e}")
            return "AI query failed"

    async def execute_android_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """Execute action on Android device via MCP"""
        try:
            response = requests.post(
                f"{self.mcp_url}/android/action",
                json=action,
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "error": f"MCP error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_todo_tasks(self) -> List[Dict[str, Any]]:
        """Read tasks from todo.md"""
        todo_file = self.workspace / 'todo.md'
        if not todo_file.exists():
            logger.warning("todo.md not found, creating default tasks")
            return self.create_default_tasks()

        try:
            with open(todo_file, 'r') as f:
                content = f.read()

            # Parse markdown tasks (basic implementation)
            tasks = []
            for line in content.split('\n'):
                if line.strip().startswith('- [ ]') or line.strip().startswith('- [x]'):
                    task_text = line.strip()[5:].strip()
                    completed = '[x]' in line
                    tasks.append({
                        'id': len(tasks) + 1,
                        'description': task_text,
                        'completed': completed,
                        'type': 'android_automation'
                    })

            return tasks
        except Exception as e:
            logger.error(f"Failed to read todo.md: {e}")
            return self.create_default_tasks()

    def create_default_tasks(self) -> List[Dict[str, Any]]:
        """Create default tasks for Android automation"""
        return [
            {
                'id': 1,
                'description': 'Take screenshot of Android home screen',
                'completed': False,
                'type': 'screenshot',
                'action': {'type': 'screenshot', 'target': 'home'}
            },
            {
                'id': 2,
                'description': 'Open Settings app',
                'completed': False,
                'type': 'app_launch',
                'action': {'type': 'launch_app', 'package': 'com.android.settings'}
            },
            {
                'id': 3,
                'description': 'Navigate through device information',
                'completed': False,
                'type': 'navigation',
                'action': {'type': 'navigate', 'target': 'device_info'}
            }
        ]

    async def execute_autonomous_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single autonomous task"""
        self.current_task = task
        logger.info(f"Executing task: {task['description']}")

        # Take initial screenshot
        screenshot_path = self.take_screenshot(f"task_{task['id']}_before.png")

        # Generate AI plan for task
        prompt = f"""
        ANDROID AUTOMATION TASK
        Task: {task['description']}
        Task Type: {task.get('type', 'general')}
        Current Screenshot: {screenshot_path}

        As an autonomous Android automation agent, create a detailed execution plan.
        Available actions via MCP server:
        - take_screenshot()
        - tap(x, y)
        - swipe(start_x, start_y, end_x, end_y)
        - type_text(text)
        - press_key(key)
        - launch_app(package_name)
        - get_current_activity()
        - scroll(direction)

        Return a JSON plan with steps to complete this task.
        """

        ai_plan = await self.query_ai_model(prompt, {'task': task})

        # Execute the plan
        results = []
        try:
            # Parse AI plan and execute steps
            if 'action' in task:
                action_result = await self.execute_android_action(task['action'])
                results.append(action_result)

            # Take final screenshot
            final_screenshot = self.take_screenshot(f"task_{task['id']}_after.png")

            # Mark task as completed
            task['completed'] = True
            task['results'] = results
            task['screenshots'] = [screenshot_path, final_screenshot]

            logger.info(f"Task {task['id']} completed successfully")
            return task

        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            task['error'] = str(e)
            return task
        finally:
            self.current_task = None

    async def run_autonomous_mode(self):
        """Run agent in autonomous mode"""
        logger.info("Starting autonomous mode")

        # Wait for Android emulator to be ready
        while not await self.check_android_connection():
            logger.info("Waiting for Android emulator...")
            await asyncio.sleep(10)

        # Wait for MCP server to be ready
        while not await self.check_mcp_connection():
            logger.info("Waiting for MCP server...")
            await asyncio.sleep(5)

        # Load tasks from todo.md
        tasks = self.read_todo_tasks()
        logger.info(f"Loaded {len(tasks)} tasks")

        # Execute tasks sequentially
        for task in tasks:
            if not task.get('completed', False):
                await self.execute_autonomous_task(task)
                await asyncio.sleep(5)  # Brief pause between tasks

        logger.info("Autonomous execution completed")

    def run(self):
        """Main entry point"""
        if self.task_mode == 'autonomous':
            # Run autonomous mode in background
            asyncio.create_task(self.run_autonomous_mode())

        # Start FastAPI server
        uvicorn.run(self.app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    agent = Play2AIAgent()
    agent.run()
