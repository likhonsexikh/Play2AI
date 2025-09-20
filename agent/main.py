import os
import subprocess

def run_command(command):
    """Runs a shell command and returns its output."""
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("Output:\n", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:\n", e.stderr)
        return e.stderr

def main():
    """Main entry point for the AI agent."""
    print("🤖 AI Agent Initializing...")

    # Example task: Check ADB connection
    print("\n--- Verifying ADB Connection ---")
    run_command("adb devices")

    # Example task: Capture screen
    print("\n--- Capturing Screen ---")
    if not os.path.exists("output"):
        os.makedirs("output")
    run_command("adb screencap -p /sdcard/screen.png")
    run_command("adb pull /sdcard/screen.png output/screenshot.png")
    print("Screenshot saved to output/screenshot.png")

    print("\n✅ Agent finished.")

if __name__ == "__main__":
    main()
