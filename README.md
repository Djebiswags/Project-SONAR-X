# Project SONAR-X

A lightweight macOS/Unix system sentinel for real-time telemetry, adaptive CPU cooling, and configurable process mitigation.

## 🧠 About
Project SONAR-X monitors system health in the background, surfaces CPU/RAM/network status in the macOS menu bar, and optionally deploys automated defensive actions using a local kill list. It is built for low-overhead operation, rapid visibility, and easy configuration on personal systems.

- **`sonar_menu.py`**: Menu-bar controller and sentinel engine.
- **`dashboard.py`**: Live telemetry HUD for CPU and RAM.
- **`sonar_core.py`**: CLI pulse engine for continuous system monitoring.
- **`config.json`**: Local process kill list for cooling-mode mitigation.
- **`mac_startup_daemon.plist`**: Launchd agent for optional persistent startup.

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
```

## ▶️ Usage
- Start the menu-bar sentinel:
  ```bash
  python3 sonar_menu.py
  ```
- Run one monitoring cycle for validation:
  ```bash
  python3 sonar_core.py --once
  ```
- Launch the HUD directly:
  ```bash
  python3 dashboard.py
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

> Note: `dashboard.py` requires a Python installation with Tkinter support. If your current Python build does not include Tkinter, the HUD will not launch.

## 📄 License
This project is released under the MIT License. See `LICENSE` for details.

## 📌 Notes
- `sonar_menu.py` launches the dashboard with the active Python interpreter.
- The application is designed for macOS, but core monitoring logic can run on other Unix-like systems.
- Use `launchctl` with `mac_startup_daemon.plist` for persistent startup on macOS.

