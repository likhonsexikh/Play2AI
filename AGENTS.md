# AGENTS.md - Play2AI Agentic AI System

## Overview

The Play2AI system implements a multi-agent architecture that enables autonomous AI agents to interact with Android emulators through a sophisticated orchestration layer. This document describes all agents, their capabilities, interactions, and the overall system architecture.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Play2AI Agentic System                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Master    │    │   Android   │    │   Vision    │         │
│  │   Agent     │◄──►│   Control   │◄──►│   Agent     │         │
│  │ (Orchestr.) │    │   Agent     │    │ (Screen AI) │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│         │                   │                   │              │
│         ▼                   ▼                   ▼              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Task      │    │   MCP       │    │   Monitor   │         │
│  │  Planner    │◄──►│  Server     │◄──►│   Agent     │         │
│  │   Agent     │    │  (DroidMind)│    │ (Logging)   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
├─────────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Docker    │    │   Android   │    │   GitHub    │         │
│  │ Container   │    │  Emulator   │    │  Actions    │         │
│  │  Runtime    │    │   (KVM)     │    │   CI/CD     │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Agent Catalog

### 1. Master Orchestrator Agent

**File**: `agent/src/main.py` (class `Play2AIAgent`)

**Purpose**: Central coordination and decision-making hub for the entire system.

**Capabilities**:
- **AI Model Integration**: Supports multiple LLMs (Claude, GPT, Gemini, Llama, Mistral)
- **Task Orchestration**: Reads `todo.md` and creates execution plans
- **Agent Communication**: Coordinates between all other agents
- **Autonomous Decision Making**: Makes real-time decisions based on Android state
- **Error Recovery**: Handles failures and implements retry logic
- **REST API**: Exposes control endpoints for external management

**Key Methods**:
```python
async def query_ai_model(prompt: str, context: Dict) -> str
async def execute_autonomous_task(task: Dict) -> Dict
async def run_autonomous_mode()
def read_todo_tasks() -> List[Dict]
```

**Configuration**:
- `AI_MODEL`: Choose AI backend (llama3, gemma, mistral, phi2, granite)
- `TASK_MODE`: Execution mode (autonomous, guided, testing, development)
- `MCP_SERVER_URL`: Connection to MCP server
- `ANDROID_EMULATOR_HOST`: Target Android emulator

---

### 2. Android Control Agent

**File**: `scripts/mcp_server.py` + DroidMind integration

**Purpose**: Direct interface for Android device manipulation and control.

**Capabilities**:
- **Device Management**: Connect via USB/TCP-IP, list devices, reboot
- **UI Automation**: Taps, swipes, text input, key presses
- **App Management**: Install, uninstall, launch, stop applications
- **File Operations**: Browse, read, write, push, pull device files
- **System Analysis**: Access logs, battery info, system properties
- **Screen Capture**: High-quality screenshots and screen recording

**MCP Actions Supported**:
```json
{
  "screenshot": "Capture device screen",
  "tap": {"x": 100, "y": 200},
  "swipe": {"start_x": 100, "start_y": 200, "end_x": 300, "end_y": 400},
  "type_text": {"text": "Hello World"},
  "press_key": {"key": "BACK|HOME|MENU"},
  "launch_app": {"package": "com.android.settings"},
  "install_apk": {"path": "/path/to/app.apk"},
  "get_current_activity": {},
  "scroll": {"direction": "up|down|left|right"}
}
```

**Security Features**:
- Command validation and sanitization
- Risk assessment for operations
- Protected path operations
- Comprehensive operation logging

---

### 3. Vision Analysis Agent

**File**: `agent/tools/vision_agent.py`

**Purpose**: Computer vision and screen analysis for intelligent Android interaction.

**Capabilities**:
- **UI Element Detection**: Identify buttons, text fields, menus
- **OCR (Text Recognition)**: Extract text from screenshots
- **Layout Analysis**: Understand screen structure and hierarchy
- **Change Detection**: Compare screenshots to detect UI changes
- **Accessibility Mapping**: Generate semantic UI maps
- **Object Recognition**: Identify app icons, images, and visual elements

**Integration Example**:
```python
class VisionAgent:
    def analyze_screen(self, screenshot_path: str) -> Dict:
        """Analyze screenshot and return UI elements"""

    def detect_clickable_elements(self, image) -> List[Dict]:
        """Find all interactive UI elements"""

    def extract_text(self, image, region=None) -> str:
        """OCR text extraction from image"""

    def compare_screens(self, before: str, after: str) -> Dict:
        """Detect changes between screenshots"""
```

---

### 4. Task Planning Agent

**File**: `agent/tools/task_planner.py`

**Purpose**: Intelligent task decomposition and execution planning.

**Capabilities**:
- **Goal Decomposition**: Break complex tasks into executable steps
- **Dependency Analysis**: Understand task prerequisites and ordering
- **Resource Planning**: Estimate time, complexity, and requirements
- **Adaptive Planning**: Modify plans based on execution results
- **Risk Assessment**: Identify potential failure points
- **Progress Tracking**: Monitor task completion and success metrics

**Planning Workflow**:
```python
class TaskPlannerAgent:
    def create_execution_plan(self, task: Dict) -> Dict:
        """Generate detailed execution plan for a task"""

    def analyze_dependencies(self, tasks: List[Dict]) -> Dict:
        """Identify task dependencies and optimal ordering"""

    def estimate_complexity(self, task: Dict) -> Dict:
        """Assess task difficulty and resource requirements"""

    def adapt_plan(self, current_plan: Dict, execution_results: List) -> Dict:
        """Modify plan based on real execution feedback"""
```

---

### 5. Monitoring & Logging Agent

**File**: `scripts/task_monitor.py`

**Purpose**: System health monitoring, logging, and performance tracking.

**Capabilities**:
- **Health Monitoring**: Track all agent and service status
- **Performance Metrics**: Measure task execution times and success rates
- **Error Tracking**: Comprehensive error logging and analysis
- **Resource Monitoring**: CPU, memory, and container resource usage
- **Alert System**: Notify on failures or performance degradation
- **Report Generation**: Create detailed execution reports

**Monitoring Targets**:
- Master Agent API health
- Android emulator connectivity
- MCP server responsiveness
- Docker container status
- Screenshot capture quality
- Task execution progress

---

### 6. Learning & Optimization Agent

**File**: `agent/tools/learning_agent.py`

**Purpose**: Continuous improvement through execution analysis and pattern learning.

**Capabilities**:
- **Pattern Recognition**: Identify successful automation patterns
- **Failure Analysis**: Learn from failed executions
- **Performance Optimization**: Improve execution speed and reliability
- **Strategy Adaptation**: Adjust approaches based on app behavior
- **Knowledge Base Building**: Create reusable automation knowledge
- **Predictive Analysis**: Anticipate UI changes and app updates

---

## 🔄 Agent Interaction Patterns

### 1. Standard Task Execution Flow

```
Master Agent → Task Planner → Android Control → Vision Analysis → Monitor
     ↓              ↓              ↓              ↓              ↓
   Reads         Creates        Executes       Analyzes       Logs
  todo.md        plan           actions        results        status
     ↓              ↓              ↓              ↓              ↓
  Coordinates → Validates → Performs UI → Verifies → Reports
  execution      steps      interactions    success   completion
```

### 2. Error Recovery Pattern

```
Monitor Agent detects failure
        ↓
Master Agent receives alert
        ↓
Vision Agent analyzes current state
        ↓
Task Planner creates recovery plan
        ↓
Android Control executes recovery
        ↓
Learning Agent records failure pattern
```

### 3. Adaptive Learning Pattern

```
Learning Agent analyzes execution history
        ↓
Identifies optimization opportunities
        ↓
Suggests improvements to Master Agent
        ↓
Master Agent updates execution strategies
        ↓
Task Planner incorporates new patterns
```

## 🚀 Deployment Configuration

### Environment Variables

| Variable | Description | Default | Agents Affected |
|----------|-------------|---------|-----------------|
| `AI_MODEL` | Primary AI backend | `llama3` | Master, Vision |
| `TASK_MODE` | Execution mode | `autonomous` | All agents |
| `ANDROID_EMULATOR_HOST` | Emulator hostname | `android-emulator` | Android Control |
| `MCP_SERVER_URL` | MCP server endpoint | `http://android-mcp:8081` | Master, Android Control |
| `SCREENSHOT_QUALITY` | Image capture quality | `high` | Vision, Monitor |
| `LOG_LEVEL` | Logging verbosity | `INFO` | All agents |
| `LEARNING_MODE` | Enable learning features | `true` | Learning Agent |

### Docker Compose Services

```yaml
services:
  play2ai-agent:        # Master Orchestrator
  android-emulator:     # Target Android environment
  android-mcp:          # MCP Server + Android Control
  task-monitor:         # Monitoring & Logging
  vision-processor:     # Vision Analysis (optional)
```

## 📊 Agent Performance Metrics

### Master Agent Metrics
- Task completion rate
- Average planning time
- Decision accuracy
- Error recovery success rate

### Android Control Agent Metrics
- Action execution time
- ADB command success rate
- Screenshot capture latency
- UI interaction accuracy

### Vision Agent Metrics
- Element detection accuracy
- OCR text recognition rate
- Change detection precision
- Processing time per frame

### System-wide Metrics
- End-to-end task completion time
- Resource utilization efficiency
- Failure rate by task type
- Learning improvement rate

## 🔧 Agent Development Guidelines

### Adding New Agents

1. **Create Agent Class**:
```python
class NewAgent:
    def __init__(self):
        self.setup_agent()

    async def execute_capability(self, params: Dict) -> Dict:
        """Main agent capability"""
        pass
```

2. **Register with Master Agent**:
```python
# In main.py
self.agents['new_agent'] = NewAgent()
```

3. **Update Docker Compose**:
```yaml
new-agent-service:
  build: ./agents/new_agent
  networks:
    - play2ai-network
```

4. **Add Monitoring**:
```python
# In task_monitor.py
await self.check_agent_health('new_agent')
```

### Agent Communication Protocol

All agents communicate via:
- **REST APIs** for synchronous operations
- **Message queues** for asynchronous events
- **Shared volumes** for file-based data exchange
- **Environment variables** for configuration

### Security Considerations

- **Sandboxing**: Each agent runs in isolated containers
- **Permission Control**: Limited file system access
- **API Authentication**: Secure inter-agent communication
- **Audit Logging**: Complete action traceability
- **Resource Limits**: CPU and memory constraints

## 📈 Future Agent Roadmap

### Planned Agents

1. **Game Strategy Agent**: Specialized for mobile game automation
2. **Data Collection Agent**: Systematic app data extraction
3. **Testing Validation Agent**: Automated quality assurance
4. **Performance Benchmark Agent**: App performance measurement
5. **Security Audit Agent**: Privacy and security analysis

### Enhancement Areas

- **Multi-device Support**: Coordinate across multiple emulators
- **Cloud Integration**: Connect with cloud-based AI services
- **Real Device Support**: Extend beyond emulators
- **Voice Control**: Add speech recognition and synthesis
- **Gesture Recognition**: Advanced touch pattern analysis

## 🤝 Contributing to Agent Development

### Development Setup
```bash
git clone https://github.com/likhonsexikh/Play2AI.git
cd Play2AI
docker compose -f docker-compose.play2ai.yml up --build
```

### Testing New Agents
```bash
# Run agent tests
python -m pytest agents/tests/

# Integration testing
docker compose exec play2ai-agent python test_agent_integration.py
```

### Agent Code Standards
- Follow PEP 8 for Python code style
- Include comprehensive docstrings
- Implement proper error handling
- Add unit tests for all capabilities
- Use async/await for I/O operations

---

*This documentation is maintained by the Play2AI development team. For questions or contributions, please open an issue in the GitHub repository.*
