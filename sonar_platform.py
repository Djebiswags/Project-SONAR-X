"""Cross-platform layer for SONAR-X.

All OS-specific behaviour lives here so ``sonar_core.py`` stays portable.
Today the project is macOS-first; this module is the bridge to Linux and
Windows without forking the codebase.

Layout
------
- ``SYSTEM``: ``"Darwin"``, ``"Linux"`` or ``"Windows"`` (from platform.system()).
- ``notify(title, message)``: desktop notification. Prefers ``plyer``
  (pip install plyer) and falls back per-OS: ``osascript`` on macOS,
  ``notify-send`` on Linux, plain print as a last resort.
- ``install_autostart(python_exe, script)`` / ``remove_autostart()``:
  run the sentinel at login. macOS -> launchd plist,
  Linux -> systemd user unit, Windows -> Startup folder batch file.
  Returns the path of the artifact created (or removed).
- ``tray_backend()``: ``"rumps"`` on macOS, ``"pystray"`` everywhere else.
  Import lazily at the call site — neither is a hard dependency here.

Wiring (next step, not done automatically):
    from sonar_platform import notify
    # in sonar_core.alert_desktop: replace the osascript call with notify(...)
"""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path

SYSTEM = platform.system()  # Darwin | Linux | Windows

APP_NAME = "SONAR-X"
LAUNCHD_LABEL = "com.sonarx.sentinel"
SYSTEMD_UNIT = "sonarx.service"
WIN_TASK_NAME = "SONAR-X Sentinel"


# ------------------------------------------------------------------ notify


def _notify_plyer(title: str, message: str) -> bool:
    try:
        from plyer import notification

        notification.notify(title=title, message=message, app_name=APP_NAME)
        return True
    except Exception:
        return False


def _notify_fallback(title: str, message: str) -> None:
    safe = message.replace('"', '\\"')
    try:
        if SYSTEM == "Darwin":
            script = f'display notification "{safe}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=False)
        elif SYSTEM == "Linux":
            subprocess.run(["notify-send", title, message], check=False)
        else:  # Windows without plyer, or anything exotic
            print(f"[{title}] {message}")
    except Exception:
        print(f"[{title}] {message}")


def notify(title: str, message: str) -> None:
    """Send a desktop notification on any supported OS. Never raises."""
    try:
        if not _notify_plyer(title, message):
            _notify_fallback(title, message)
    except Exception:
        print(f"[{title}] {message}")


# ---------------------------------------------------------------- autostart


def _launchd_plist(python_exe: str, script: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" \
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>{LAUNCHD_LABEL}</string>
    <key>ProgramArguments</key>
    <array><string>{python_exe}</string><string>{script}</string></array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>
"""


def _systemd_unit(python_exe: str, script: str) -> str:
    return f"""[Unit]
Description=SONAR-X system sentinel
After=graphical-session.target

[Service]
ExecStart={python_exe} {script}
Restart=on-failure

[Install]
WantedBy=default.target
"""


def _windows_bat(python_exe: str, script: str) -> str:
    return f'@echo off\r\nstart "" "{python_exe}" "{script}"\r\n'


def _autostart_path() -> Path:
    home = Path.home()
    if SYSTEM == "Darwin":
        return home / "Library" / "LaunchAgents" / f"{LAUNCHD_LABEL}.plist"
    if SYSTEM == "Linux":
        return home / ".config" / "systemd" / "user" / SYSTEMD_UNIT
    # Windows
    appdata = os.environ.get("APPDATA", str(home))
    return (
        Path(appdata)
        / "Microsoft"
        / "Windows"
        / "Start Menu"
        / "Programs"
        / "Startup"
        / "sonarx.bat"
    )


def install_autostart(python_exe: str, script: str) -> Path:
    """Write the OS-native autostart artifact. Returns its path."""
    dest = _autostart_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    if SYSTEM == "Darwin":
        content = _launchd_plist(python_exe, script)
    elif SYSTEM == "Linux":
        content = _systemd_unit(python_exe, script)
    else:
        content = _windows_bat(python_exe, script)
    dest.write_text(content, encoding="utf-8")
    return dest


def remove_autostart() -> bool:
    """Remove the autostart artifact. Returns True if one existed."""
    dest = _autostart_path()
    if dest.exists():
        dest.unlink()
        return True
    return False


def post_install_hint() -> str:
    """One-liner the user should run after install_autostart(), per OS."""
    if SYSTEM == "Darwin":
        return (
            f"launchctl load ~/Library/LaunchAgents/{LAUNCHD_LABEL}.plist"
        )
    if SYSTEM == "Linux":
        return "systemctl --user daemon-reload && systemctl --user enable --now sonarx.service"
    return "Log out and back in (Startup folder entry runs automatically)."


# --------------------------------------------------------------------- tray


def tray_backend() -> str:
    """Which tray library the menu-bar app should import: rumps or pystray."""
    return "rumps" if SYSTEM == "Darwin" else "pystray"
