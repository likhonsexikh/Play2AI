# 📝 Tasks for Agent (First Iteration)

**Note:** To run the tasks below, you must provide a sample APK file. You can do this by adding a volume mount to `docker-compose.yml` and passing the `--apk-path` argument to the agent in the GitHub workflow.

For the next run, the agent should complete the following tasks in order:

1. Install a sample Android app (e.g. Calculator APK) on the emulator
2. Open the app
3. Perform a simple interaction (e.g. press a button in the app)
4. Capture a screenshot after interaction
5. Save the screenshot to a shared folder `/app/output/screenshots`
6. Generate a short text summary describing whether the interaction succeeded, based on the screenshot
7. Log all steps in `/app/output/logs/run1.log`
