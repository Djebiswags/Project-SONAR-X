# Project SONAR-X: Automated System Sentinel

Project SONAR-X is a lightweight, automated telemetry daemon built for macOS. It acts as a smart guard dog for computer systems, monitoring hardware health and network status in real-time, and executing automated defensive protocols before system failure occurs.

## Core Architecture & Features
* **Real-Time Telemetry:** Monitors CPU load via `psutil` within a dedicated background thread.
* **Network Sniffer:** Continuously pings external servers to verify active internet connection status.
* **Automated Cooling Protocol:** Integrates with local software to automatically reduce system load (e.g., dropping audio volumes) when the CPU redlines past 85%.
* **macOS Daemon Integration:** Runs headlessly in the macOS Menu Bar utilizing `rumps` and a custom `launchctl` `.plist` agent for persistent startup execution.
* **Hot-Key Macros:** Global keyboard listeners via `pynput` for instant system-wide script execution.

## Deployment
See `requirements.txt` for Python dependencies. The application is designed to be loaded into the macOS user space via the included `mac_startup_daemon.plist`.
=======
# Project SONAR-X
A high-performance macOS system daemon and telemetry suite.

## Features
- Persistent background monitoring using `launchd`.
- Asynchronous resource optimization via intelligent process termination.
- Custom GUI dashboard for real-time system telemetry.

## Deployment
1. Clone the repository.
2. Setup the virtual environment: `python3 -m venv agent_env`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Deploy the daemon: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.sonarx.app.plist`.
