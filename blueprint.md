# 📘 Blueprint: Agentic AI + Android Emulator (Dockerized)

## 🎯 Goal
Build a **chatbot with agentic AI control** that can:
- Run inside **Docker** containers
- Mount and control an **Android emulator** (Waydroid / Genymotion / Android Studio Emulator / Anbox)
- Execute **autonomous tasks** (install apps, simulate taps, capture screen, analyze results)
- Be orchestrated via **GitHub Actions** using a `model-runner` workflow
- Follow structured tasks defined in `todo.md`

---

## 🏗️ System Architecture

### 1. **AI Layer (Agent)**
- Powered by LLMs (OpenAI GPT, Gemini, or Ollama local models)
- Runs inside Docker
- Exposed as a service with a chat interface
- Has tool access to:
  - `adb` (install apps, tap, swipe, input text)
  - `scrcpy` (screen mirroring for vision feedback)
  - File system mounts

### 2. **Android Emulator Layer**
- Options:
  - **Waydroid** → Best for container performance
  - **Genymotion** → Cloud/device testing
  - **Android Studio Emulator** → Full SDK
  - **Anbox** → Lightweight apps
- Mounted into Docker with GPU passthrough for high-performance tasks

### 3. **Control Bridge**
- AI issues structured commands
- Python/Node.js runtime handles:
  - `adb install <apk>`
  - `adb shell input tap <x> <y>`
  - `adb screencap`
- Loop: AI → Command → Emulator → Feedback

### 4. **CI/CD & Automation**
- GitHub repo contains:
  - `blueprint.md` (this file)
  - `todo.md` (task definitions for AI)
  - `docker-compose.yml` (multi-service stack)
  - `agent/` (runtime code)
  - `.github/workflows/model-runner.yml` (orchestrates AI execution)
- GitHub Actions job:
  - Spins up Docker services
  - Mounts emulator
  - Runs AI agent to process `todo.md`
  - Reports results in PR/issue

---

## 🚦 Development Flow
1. **Plan** → `blueprint.md` (current step)
2. **Scaffold Repo** → initialize Docker + agent runtime
3. **Integrate GitHub Actions** → add `model-runner.yml`
4. **Define Tasks** → add `todo.md` with structured goals
5. **Run Autonomous Cycles** → AI agent executes tasks, reports back
6. **Iterate** → extend tools (vision models, more emulator control, external APIs)

---

## 🔒 Security & Safety
- Emulator isolated in container (no root on host)
- AI only allowed to use defined tools (`adb`, `scrcpy`, file I/O)
- API keys stored in `.env` or GitHub Secrets
- Safe fallback: manual approval for destructive actions

---

## ✅ Next Steps
- [ ] Create initial repo structure
- [ ] Add Dockerfiles & `docker-compose.yml`
- [ ] Implement AI agent runtime (Python/Node.js)
- [ ] Add GitHub Actions workflow (`model-runner.yml`)
- [ ] Write `todo.md` for first autonomous tasks
