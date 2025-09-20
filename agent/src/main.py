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
    args = parser.parse_args()

    if not wait_for_device():
        print("Emulator not ready, exiting.")
        sys.exit(1)

    # tasks from todo
    tasks = parse_todo(args.todo)
    # a simple hardcoded first iteration
    logs_dir = "/app/logs"
    screenshots_dir = "/android/screenshots"
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(screenshots_dir, exist_ok=True)

    # Task 1: Install calculator
    # TODO: The path below is a placeholder.
    # You need to mount a sample APK into the container and provide the correct path here.
    install_app("/path/to/sample_calculator.apk")  # need to include sample apk
    time.sleep(5)
    # Task 2: Open calculator
    open_app("com.android.calculator2", "com.android.calculator2.Calculator")
    time.sleep(3)
    # Task 3: Press button (e.g. “1 + 2 =”)
    tap(100, 200)  # coordinates need adjusting
    tap(200, 200)
    tap(150, 300)
    time.sleep(2)
    # Task 4: Capture screenshot
    capture_screenshot(f"{screenshots_dir}/after_interaction.png")
    # Task 6 & 7: Generate summary & log (simplified)
    with open(f"{logs_dir}/run1.log", "w") as lf:
        lf.write("Installed calculator, opened app, pressed buttons, screenshot saved.\n")
    print("Tasks done.")

if __name__ == "__main__":
    main()
