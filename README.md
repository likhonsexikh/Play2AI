# Play2AI

Agentic AI + Android Emulator Platform.
Allows an AI agent to autonomously run tasks inside an Android emulator, all containerized via Docker, orchestrated via GitHub Actions.

---

## 🔍 Contents

- `blueprint.md` — overall system plan
- `todo.md` — list of tasks/goals for the agent to execute
- `agent/` — source code for the agent runtime
- `docker-compose.yml` — defines services (agent, emulator, etc.)
- `.github/workflows/model-runner.yml` — CI workflow for executing tasks
- Other config / scripts for emulator control (adb, scrcpy etc.)

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- (Optional) GPU / KVM support for hardware acceleration
- Access to an LLM (OpenAI, Gemini, or local model)
- GitHub account + ability to set up Actions

### Local setup

```bash
git clone https://github.com/likhonsexikh/Play2AI.git
cd Play2AI

# build + run containers
docker-compose up --build
```

The agent container runs the AI agent runtime.

The emulator container runs the Android emulator (Waydroid / alternative).

The agent should be able to see and control the emulator via adb.

### GitHub Actions

The workflow defined in `.github/workflows/model-runner.yml` will:

- Spin up necessary docker services
- Provide `todo.md` to the agent runtime
- Let the agent perform tasks
- Save logs/screenshots as artifacts

---

## 🛠️ Project Structure

```
.
├── blueprint.md
├── README.md
├── todo.md
├── docker-compose.yml
├── agent/
│   ├── Dockerfile
│   ├── src/
│   │   ├── main.py (or index.js)
│   │   └── tools/ (adb wrapper, screen capture etc.)
├── emulator/  (optional, configuration or scripts for emulator)
└── .github/
    └── workflows/
        └── model-runner.yml
```

---

## 🎯 Usage

1. Edit `todo.md` to define the tasks you want the agent to execute.
2. Commit & push. Either run locally (`docker-compose`) or via GitHub Actions.
3. Review results: look at logs, artifacts.
4. Iterate: refine tools, emulator control, feedback loop.

---

## 🧰 Tools & Dependencies

- adb — Android Debug Bridge
- scrcpy or screen capture utility
- Python or Node.js for agent runtime
- Docker / Docker Compose
- LLM backend credentials and APIs

---

## 🤝 Contributing

Contributions, ideas, issues are welcome. If you implement new emulator features (e.g. game-optimized), vision models, tools, or UI, please open PRs.

---

## ⚠️ Security Notes

- Do not commit secrets / credentials.
- Limit the agent’s permissions.
- Use container isolation.
