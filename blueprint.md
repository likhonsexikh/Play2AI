# 📘 Blueprint: Agentic AI + Android Emulator (Dockerized)

## 🎯 Goal
Build a **chatbot with agentic AI control** that can:
- Run inside **Docker** containers
- Mount and control an **Android emulator** (Waydroid / Genymotion / Android Studio Emulator / Anbox)
- Execute **autonomous tasks** (install apps, simulate taps/swipes, capture screen, analyze results)
- Be orchestrated via **GitHub Actions** using a `model-runner` workflow
- Follow structured tasks defined in `todo.md`

---

## 🏗️ System Architecture

### 1. **AI Layer (Agent)**
- Powered by LLMs (OpenAI GPT, Gemini, or local models via Ollama)
- Runs inside Docker
- Exposed as a service with a chat or command-interface
- Has tool access to:
  - `adb` (install apps, taps, swipes, input text)
  - `scrcpy` or other screen capture for feedback
  - File system mounts for persistence and artifacts

### 2. **Android Emulator Layer**
- Optionally:
  - **Waydroid** → best for container-performance
  - **Genymotion** → cloud or local device options
  - **Android Studio Emulator** → full SDK & dev features
  - **Anbox** → lightweight sandboxed apps
- Mount emulator into Docker with GPU / binder / kvm passthrough as needed

### 3. **Control Bridge**
- AI issues structured commands (via JSON or CLI)
- Runtime (Python or Node.js) executes them, monitors status, captures feedback (screenshots, logs)
- Feedback loop: AI → Command → Emulator → Feedback → AI

### 4. **CI/CD & Automation**
- Repo contains:
  - `blueprint.md` (this file)
  - `todo.md` (task definitions)
  - `docker-compose.yml` (multi-service stack)
  - `agent/` (runtime code)
  - `.github/workflows/model-runner.yml` (workflow to run tasks)
- GitHub Actions job(s):
  - Set up the emulator + agent containers
  - Provide `todo.md` to the agent
  - Have the agent execute tasks
  - Report results (logs, screenshots, status) back, possibly via PR/issue comments or artifacts

---

## 🚦 Development Flow
1. **Plan** → finalize `blueprint.md`
2. **Scaffold Repo** → init directory structure, Dockerfiles, runtime code
3. **GitHub Actions** → add `model-runner.yml` workflow
4. **Define Tasks** → use `todo.md` for first iteration tasks
5. **Agent Execution** → run via GitHub Actions (or locally) to complete tasks
6. **Feedback & Iterate** → improve controls, add more tools, handle vision, etc.

---

## 🔒 Security & Safety
- Run emulator inside isolated container (minimize privileges)
- Limit AI’s tool-access to only safe commands (adb, scrcpy, file safety)
- Use GitHub Secrets for API keys etc.
- Possibly require manual confirmations for destructive or system-level commands

---

## ✅ Next Steps
- [ ] Create initial repo structure (agent code, emulator config, docker-compose)
- [ ] Write Dockerfiles and `docker-compose.yml`
- [ ] Implement AI agent runtime (Python/Node.js)
- [ ] Add GitHub Actions workflow (`model-runner.yml`)
- [ ] Create `todo.md` for first tasks
- [ ] Test locally and via GitHub Actions
- [ ] Add logging, artifact capture (screenshots, logs)
