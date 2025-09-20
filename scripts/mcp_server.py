#!/usr/bin/env python3
"""
MCP Server wrapper for Android control
"""
import os
import json
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI
import uvicorn
import subprocess
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Android MCP Server", version="1.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mcp_server": "running"}

@app.post("/android/action")
async def execute_android_action(action: Dict[str, Any]):
    """Execute Android action via ADB/DroidMind"""
    try:
        action_type = action.get('type', '')

        if action_type == 'screenshot':
            result = subprocess.run([
                'adb', 'exec-out', 'screencap', '-p'
            ], capture_output=True, timeout=30)

            if result.returncode == 0:
                return {"success": True, "screenshot_data": "captured"}
            else:
                return {"success": False, "error": result.stderr.decode()}

        elif action_type == 'tap':
            x, y = action.get('x', 0), action.get('y', 0)
            result = subprocess.run([
                'adb', 'shell', 'input', 'tap', str(x), str(y)
            ], capture_output=True, timeout=10)
            return {"success": result.returncode == 0}

        elif action_type == 'launch_app':
            package = action.get('package', '')
            result = subprocess.run([
                'adb', 'shell', 'monkey', '-p', package, '-c', 'android.intent.category.LAUNCHER', '1'
            ], capture_output=True, timeout=15)
            return {"success": result.returncode == 0}

        else:
            return {"success": False, "error": f"Unknown action type: {action_type}"}

    except Exception as e:
        logger.error(f"Action execution failed: {e}")
        return {"success": False, "error": str(e)}

@app.get("/android/devices")
async def list_android_devices():
    """List connected Android devices"""
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip() and '\t' in line:
                    device_id, status = line.strip().split('\t')
                    devices.append({"id": device_id, "status": status})
            return {"success": True, "devices": devices}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
