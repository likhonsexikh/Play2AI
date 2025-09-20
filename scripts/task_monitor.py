#!/usr/bin/env python3
"""
Task Monitor for Play2AI system
"""
import os
import time
import json
import logging
import requests
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_system():
    agent_url = os.getenv('AGENT_URL', 'http://play2ai-agent:8080')
    mcp_url = os.getenv('MCP_URL', 'http://android-mcp:8081')

    while True:
        try:
            # Check agent status
            agent_response = requests.get(f"{agent_url}/status", timeout=5)
            if agent_response.status_code == 200:
                status = agent_response.json()
                logger.info(f"Agent Status: {status}")

            # Check MCP server
            mcp_response = requests.get(f"{mcp_url}/health", timeout=5)
            if mcp_response.status_code == 200:
                logger.info("MCP Server: healthy")

            time.sleep(30)  # Monitor every 30 seconds

        except Exception as e:
            logger.warning(f"Monitor check failed: {e}")
            time.sleep(60)

if __name__ == "__main__":
    monitor_system()
