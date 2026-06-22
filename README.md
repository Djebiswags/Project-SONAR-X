# Project SONAR-X

A lightweight macOS/Unix system sentinel for real-time telemetry, adaptive CPU cooling, and configurable process defense.

## 🧠 About
Project SONAR-X is built for fast system health insights, low-overhead background monitoring, and automated mitigation using a local kill list and live HUD. It is designed for easy AI discoverability with focused keywords: telemetry, macOS menu bar, process management, system sentinel, live HUD.

- **`sonar_menu.py`**: Menu-bar app and sentinel controller.
- **`dashboard.py`**: Live telemetry HUD showing CPU and RAM usage.
- **`sonar_core.py`**: CLI pulse engine for system monitoring.
- **`config.json`**: Process kill list for automated cooling mode.
- **`mac_startup_daemon.plist`**: macOS launchd agent for persistent startup.

## ✨ Features
- Start and stop monitoring from the macOS menu bar.
- Live CPU and network status updates.
- Automated cooling mode when CPU load exceeds thresholds.
- Config-driven process mitigation based on `config.json`.
- Desktop notifications for status changes and critical events.

## 🧩 Requirements
- Python 3.10+
- `psutil`
- `requests`
- `rumps`
- `customtkinter`

## 🚀 Installation

```bash
git clone https://github.com/Djebiswags/Project-SONAR-X.git
cd Project-SONAR-X
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 sonar_menu.py
```

## ⚙️ Configuration
Create a local `config.json` from the tracked template:

```bash
cp config.example.json config.json
```

Then update `config.json` to customize which processes can be terminated during high CPU load.

```json
{
    "kill_list": [
        "Google Chrome Helper",
        "OneDrive",
        "Dropbox",
        "Adobe Desktop Service",
        "Creative Cloud",
        "Spotify",
        "EpicGamesLauncher"
    ]
}
```

## 🧪 Running the HUD
Launch the HUD from the menu bar using the `📊 Launch Visual HUD` action, or run:

```bash
python3 dashboard.py
```

## � License
This project is released under the MIT License. See `LICENSE` for details.

## �📌 Notes
- `sonar_menu.py` launches the dashboard with the active Python interpreter.
- The application is designed for macOS, but core monitoring logic can run on other Unix-like systems.
- Use `launchctl` with `mac_startup_daemon.plist` for persistent startup on macOS.

