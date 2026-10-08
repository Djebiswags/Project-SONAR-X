"""Linux system-tray frontend for SONAR-X.

pystray counterpart to the macOS ``sonar_menu.py``: start/stop the sentinel
from the tray, live CPU/network status in the menu, cooling mode with the
config kill list, and one-click HUD launch.

Run:
    python3 sonar_tray.py

Requires: pystray, pillow, psutil, requests
"""

from __future__ import annotations

import subprocess
import sys
import threading
import time
from pathlib import Path

import psutil
import pystray
from PIL import Image, ImageDraw

from sonar_core import (
    APP_NAME,
    DEFAULT_CPU_THRESHOLD,
    check_network,
    execute_silent_kill,
    load_config,
)
from sonar_platform import notify

TICK_SECONDS = 5
COOLING_RECOVER_BELOW = 60.0


def build_icon_image(size: int = 64, cooling: bool = False) -> Image.Image:
    """Render the tray icon (sonar rings + blip). Teal = normal, blue = cooling."""
    img = Image.new("RGBA", (size, size), (16, 20, 28, 255))
    draw = ImageDraw.Draw(img)
    cx = cy = size // 2
    ring = (45, 212, 191, 255) if not cooling else (147, 197, 253, 255)
    for radius in (size // 2 - 4, size // 3, size // 6):
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=ring,
            width=2,
        )
    dot = (52, 211, 153, 255) if not cooling else (96, 165, 250, 255)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=dot)
    return img


class SonarXTray:
    def __init__(self) -> None:
        self.monitoring = False
        self.is_cooling = False
        self.kill_list = load_config()
        self.status_text = f"\U0001f3a7 {APP_NAME}"
        self._stop = threading.Event()
        # the status line's text is a callable, so update_menu() re-renders
        # it with the latest status_text
        self.icon = pystray.Icon(
            "sonar-x", build_icon_image(), APP_NAME, self.make_menu()
        )

    # ------------------------------------------------------------------ menu

    def make_menu(self) -> pystray.Menu:
        return pystray.Menu(
            pystray.MenuItem(lambda _item: self.status_text, None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("\u25b6\ufe0f Start / Stop Sentinel", self.toggle_monitoring),
            pystray.MenuItem("\U0001f4ca Launch Visual HUD", self.open_dashboard),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self.quit),
        )

    def refresh(self) -> None:
        """Push new icon art + rebuilt menu to the tray. Never raises."""
        try:
            self.icon.icon = build_icon_image(cooling=self.is_cooling)
            self.icon.update_menu()
        except Exception:
            pass

    # --------------------------------------------------------------- actions

    def toggle_monitoring(self, _icon=None, _item=None) -> None:
        self.monitoring = not self.monitoring
        if self.monitoring:
            self._stop.clear()
            threading.Thread(target=self.heartbeat_loop, daemon=True).start()
            notify(APP_NAME, "Agent Online — defensive systems active.")
        else:
            self._stop.set()
            self.is_cooling = False
            self.status_text = f"\U0001f3a7 {APP_NAME}"
            self.refresh()
            notify(APP_NAME, "Agent Offline — standing down.")

    def open_dashboard(self, _icon=None, _item=None) -> None:
        dashboard = Path(__file__).with_name("dashboard.py")
        subprocess.Popen([sys.executable, str(dashboard)])

    def quit(self, icon=None, _item=None) -> None:
        self.monitoring = False
        self._stop.set()
        (icon or self.icon).stop()

    # -------------------------------------------------------------- engine

    def heartbeat_tick(self) -> None:
        """One 5-second monitoring cycle. Factored out for testability."""
        cpu_load = psutil.cpu_percent(interval=2)
        net_icon = "\U0001f7e2" if check_network() == "ONLINE" else "\U0001f534"

        if self.is_cooling:
            self.status_text = f"\u2744\ufe0f COOLING: {cpu_load}% | {net_icon}"
            if cpu_load < COOLING_RECOVER_BELOW:
                self.is_cooling = False
                notify(APP_NAME, "System stable. Resuming standard operations.")
        else:
            if cpu_load > DEFAULT_CPU_THRESHOLD:
                self.is_cooling = True
                kills = execute_silent_kill(self.kill_list)
                notify(APP_NAME, f"REDLINE! Terminated {kills} background hogs.")
            self.status_text = f"\U0001f3a7 CPU: {cpu_load}% | {net_icon}"
        self.refresh()

    def heartbeat_loop(self) -> None:
        while self.monitoring and not self._stop.is_set():
            self.heartbeat_tick()
            self._stop.wait(TICK_SECONDS)

    def run(self) -> None:
        self.icon.run()


if __name__ == "__main__":
    SonarXTray().run()
