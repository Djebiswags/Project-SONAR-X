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
    """Radar-sweep tray icon: dark rounded tile, rings, sweep wedge, blip.

    Teal = normal, blue = cooling.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [2, 2, size - 3, size - 3], radius=14, fill=(13, 17, 23, 255)
    )
    cx = cy = size // 2
    ring = (96, 165, 250, 255) if cooling else (45, 212, 191, 255)
    for radius in (size * 3 // 8, size // 4, size // 8):
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=ring,
            width=2,
        )
    # sweep wedge on its own layer so it can be translucent
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    wedge = ImageDraw.Draw(layer)
    sweep = (200, 225, 255, 110) if cooling else (190, 255, 240, 110)
    outer = size * 3 // 8
    wedge.pieslice(
        [cx - outer, cy - outer, cx + outer, cy + outer],
        start=-70,
        end=-15,
        fill=sweep,
    )
    img = Image.alpha_composite(img, layer)
    draw = ImageDraw.Draw(img)
    dot = (147, 197, 253, 255) if cooling else (52, 211, 153, 255)
    bx, by = size // 8, -(size // 4 - 2)
    draw.ellipse([cx + bx - 3, cy + by - 3, cx + bx + 3, cy + by + 3], fill=dot)
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

    def hud_readiness(self) -> str | None:
        """None if the HUD can launch, else a human-readable reason it can't."""
        if not Path(__file__).with_name("dashboard.py").exists():
            return "dashboard.py not found next to the tray app"
        try:
            import tkinter  # noqa: F401
        except ImportError:
            return "python3-tk is not installed (sudo apt install python3-tk)"
        try:
            import customtkinter  # noqa: F401
        except ImportError:
            return "customtkinter is not installed (pip install customtkinter)"
        return None

    def open_dashboard(self, _icon=None, _item=None) -> None:
        problem = self.hud_readiness()
        if problem:
            notify(APP_NAME, f"HUD unavailable — {problem}.")
            return
        dashboard = Path(__file__).with_name("dashboard.py")
        try:
            subprocess.Popen([sys.executable, str(dashboard)])
        except Exception as exc:
            notify(APP_NAME, f"HUD failed to launch: {exc}")

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
