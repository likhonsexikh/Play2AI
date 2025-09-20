import sys
import os
import subprocess
import time
import argparse
from typing import List

def run_cmd(cmd: List[str]):
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)
    return result

def wait_for_device(timeout=120):
    start = time.time()
    while time.time() - start < timeout:
        res = run_cmd(["adb", "devices"])
        if "device" in res.stdout.splitlines()[-1]:
            return True
        time.sleep(5)
    return False

def install_app(apk_path: str):
    return run_cmd(["adb", "install", apk_path])

def open_app(package_name: str, activity: str):
    return run_cmd(["adb", "shell", "am", "start", "-n", f"{package_name}/{activity}"])

def tap(x: int, y: int):
    return run_cmd(["adb", "shell", "input", "tap", str(x), str(y)])

def capture_screenshot(save_path: str):
    tmp = "/sdcard/screen.png"
    run_cmd(["adb", "shell", "screencap", "-p", tmp])
    run_cmd(["adb", "pull", tmp, save_path])

def parse_todo(todo_fp: str):
    with open(todo_fp, "r") as f:
        lines = f.readlines()
    # Simple parsing: numbered tasks
    tasks = [line.strip() for line in lines if line.strip().startswith("1.") or line.strip().startswith("2.") or line.strip().startswith("3.")]
    return tasks

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--todo", required=True, help="Path to todo.md")
    parser.add_argument("--apk-path", required=False, help="Path to the sample APK to install.")
    args = parser.parse_args()

    if not wait_for_device():
        print("Emulator not ready, exiting.")
        sys.exit(1)

    # tasks from todo
    tasks = parse_todo(args.todo)
    # a simple hardcoded first iteration
    logs_dir = "/app/output/logs"
    screenshots_dir = "/app/output/screenshots"
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)

    # --- Task Execution Logic ---
    # This is a placeholder for a more sophisticated task runner.
    # For now, it only runs the hardcoded app interaction task if an APK is provided.
    if args.apk_path:
        print(f"--- Running App Interaction Task (APK: {args.apk_path}) ---")
        # Task 1: Install app
        install_app(args.apk_path)
        time.sleep(5)
        # Task 2: Open app
        open_app("com.android.calculator2", "com.android.calculator2.Calculator")
        time.sleep(3)
        # Task 3: Press button
        tap(100, 200)  # coordinates need adjusting
        tap(200, 200)
        tap(150, 300)
        time.sleep(2)
        # Task 4: Capture screenshot
        capture_screenshot(f"{screenshots_dir}/after_interaction.png")
        # Task 5: Log results
        with open(f"{logs_dir}/run1.log", "w") as lf:
            lf.write("Installed calculator, opened app, pressed buttons, screenshot saved.\n")
    else:
        print("--- No APK provided, skipping app interaction task ---")
        with open(f"{logs_dir}/run1.log", "w") as lf:
            lf.write("Agent initialized successfully. No APK provided, so no tasks were run.\n")

    print("✅ Agent finished.")

if __name__ == "__main__":
    main()
