"""Smoke test: boot the real pystray tray under a virtual display.

Usage:
    xvfb-run -a python3 scripts/tray_smoke.py

Exercises the actual pystray backend (not the stub): icon construction,
menu rendering, sentinel start/stop, one live heartbeat tick, and quit.
"""
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import sonar_tray


def main() -> None:
    t = sonar_tray.SonarXTray()
    assert t.icon.menu.items[0].text.startswith("\U0001f3a7"), "status line missing"

    runner = threading.Thread(target=t.run, daemon=True)
    runner.start()
    time.sleep(2)
    assert runner.is_alive(), "tray thread died"

    t.toggle_monitoring()
    assert t.monitoring, "sentinel did not start"
    time.sleep(8)  # heartbeat_tick blocks 2s in cpu_percent(interval=2)
    status = t.icon.menu.items[0].text
    assert "CPU:" in status, f"no live status after tick: {status!r}"

    t.toggle_monitoring()
    assert not t.monitoring, "sentinel did not stop"
    t.quit()
    print("tray smoke OK")


if __name__ == "__main__":
    main()
