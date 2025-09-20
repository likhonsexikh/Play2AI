# ✅ To-Do List

## 🚀 Milestone 1: Basic Setup & Sanity Check

- [ ] **Task 1: Verify Emulator Access**
  - **Goal:** Confirm the agent can communicate with the Android emulator.
  - **Steps:**
    1. Run `adb devices` to list connected devices.
    2. Capture the screen using `adb screencap`.
    3. Save the screenshot to `output/screenshot.png`.
  - **Success:** The agent successfully executes ADB commands and saves a screenshot.

- [ ] **Task 2: Install an App**
  - **Goal:** Install a simple APK on the emulator.
  - **Steps:**
    1. Download a small, open-source APK (e.g., a simple calculator app).
    2. Use `adb install <path_to_apk>` to install it.
    3. Verify the app is listed in `adb shell pm list packages`.
  - **Success:** The app is successfully installed on the emulator.
