"""Headless tests for sonar_tray.py.

pystray needs a display server, so it is stubbed out before import. What is
tested here is the tray *logic*: icon art, menu structure, the start/stop
state machine, and the heartbeat cycle (cooling entry + recovery).
"""
import sys
import types
from unittest.mock import patch

import pytest

# ---------------------------------------------------------------- pystray stub
fake_pystray = types.ModuleType("pystray")


class _MenuItem:
    def __init__(self, text, action, enabled=True):
        self.text = text
        self.action = action
        self.enabled = enabled


class _Menu(list):
    SEPARATOR = "---"

    def __init__(self, *items):
        super().__init__(items)


class _Icon:
    def __init__(self, name, icon, title, menu):
        self.name = name
        self.icon = icon
        self.title = title
        self.menu = menu
        self.stopped = False
        self.updated = 0

    def update_menu(self):
        # real pystray re-renders item texts (callables) here
        self.updated += 1

    def run(self):
        pass

    def stop(self):
        self.stopped = True


fake_pystray.MenuItem = _MenuItem
fake_pystray.Menu = _Menu
fake_pystray.Icon = _Icon
sys.modules["pystray"] = fake_pystray

pytest.importorskip("PIL")

import sonar_tray  # noqa: E402


@pytest.fixture()
def tray():
    return sonar_tray.SonarXTray()


def test_icon_image_is_rgba_square():
    img = sonar_tray.build_icon_image()
    assert img.size == (64, 64)
    assert img.mode == "RGBA"


def test_icon_image_changes_with_cooling():
    normal = sonar_tray.build_icon_image(cooling=False)
    cooling = sonar_tray.build_icon_image(cooling=True)
    assert list(normal.getdata()) != list(cooling.getdata())


def _item_text(item):
    return item.text(item) if callable(item.text) else item.text


def test_menu_structure(tray):
    menu = tray.icon.menu
    texts = [_item_text(i) for i in menu if isinstance(i, _MenuItem)]
    assert any("Start / Stop" in t for t in texts)
    assert any("HUD" in t for t in texts)
    assert "Quit" in texts
    assert texts[0] == tray.status_text  # status line is first + disabled
    assert menu[0].enabled is False


def test_toggle_starts_and_stops(tray):
    with patch.object(sonar_tray, "notify"):
        tray.toggle_monitoring()
        assert tray.monitoring is True
        tray.toggle_monitoring()
        assert tray.monitoring is False
        assert tray.is_cooling is False


def test_heartbeat_tick_normal_load(tray):
    with patch.object(sonar_tray.psutil, "cpu_percent", return_value=23.0), patch.object(
        sonar_tray, "check_network", return_value="ONLINE"
    ), patch.object(sonar_tray, "notify") as notify:
        tray.heartbeat_tick()
    assert "CPU: 23.0%" in tray.status_text
    assert tray.is_cooling is False
    notify.assert_not_called()


def test_heartbeat_tick_enters_cooling_and_kills(tray):
    tray.kill_list = ["Spotify"]
    with patch.object(sonar_tray.psutil, "cpu_percent", return_value=95.0), patch.object(
        sonar_tray, "check_network", return_value="OFFLINE"
    ), patch.object(
        sonar_tray, "execute_silent_kill", return_value=2
    ) as kill, patch.object(
        sonar_tray, "notify"
    ) as notify:
        tray.heartbeat_tick()
    assert tray.is_cooling is True
    kill.assert_called_once_with(["Spotify"])
    notify.assert_called_once()
    assert "2 background hogs" in notify.call_args[0][1]
    # next tick renders the cooling banner (same cadence as sonar_menu.py)
    with patch.object(sonar_tray.psutil, "cpu_percent", return_value=95.0), patch.object(
        sonar_tray, "check_network", return_value="OFFLINE"
    ), patch.object(sonar_tray, "notify"):
        tray.heartbeat_tick()
    assert "COOLING" in tray.status_text


def test_heartbeat_tick_recovers_below_threshold(tray):
    tray.is_cooling = True
    with patch.object(sonar_tray.psutil, "cpu_percent", return_value=40.0), patch.object(
        sonar_tray, "check_network", return_value="ONLINE"
    ), patch.object(sonar_tray, "notify") as notify:
        tray.heartbeat_tick()
    assert tray.is_cooling is False
    notify.assert_called_once()
    assert "stable" in notify.call_args[0][1]


def test_quit_stops_icon(tray):
    tray.monitoring = True
    tray.quit()
    assert tray.monitoring is False
    assert tray.icon.stopped is True


# ------------------------------------------------------- HUD launch guard


def _tray_with_dashboard(monkeypatch, tmp_path):
    monkeypatch.setattr(sonar_tray, "__file__", str(tmp_path / "sonar_tray.py"))
    (tmp_path / "dashboard.py").write_text("# stub dashboard")
    return sonar_tray.SonarXTray()


def test_hud_readiness_ok_when_gui_stack_present(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "tkinter", types.ModuleType("tkinter"))
    monkeypatch.setitem(sys.modules, "customtkinter", types.ModuleType("customtkinter"))
    tray = _tray_with_dashboard(monkeypatch, tmp_path)
    assert tray.hud_readiness() is None


def test_hud_readiness_reports_missing_dashboard(monkeypatch, tmp_path):
    monkeypatch.setattr(sonar_tray, "__file__", str(tmp_path / "sonar_tray.py"))
    tray = sonar_tray.SonarXTray()
    assert "dashboard.py not found" in tray.hud_readiness()


def test_hud_readiness_reports_missing_tkinter(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "tkinter", None)  # -> ImportError on import
    tray = _tray_with_dashboard(monkeypatch, tmp_path)
    assert "python3-tk" in tray.hud_readiness()


def test_hud_readiness_reports_missing_customtkinter(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "tkinter", types.ModuleType("tkinter"))
    monkeypatch.setitem(sys.modules, "customtkinter", None)
    tray = _tray_with_dashboard(monkeypatch, tmp_path)
    assert "customtkinter" in tray.hud_readiness()


def test_open_dashboard_notifies_and_skips_popen_when_not_ready(tray):
    with patch.object(tray, "hud_readiness", return_value="nope"), patch.object(
        sonar_tray, "notify"
    ) as notify, patch.object(sonar_tray.subprocess, "Popen") as popen:
        tray.open_dashboard()
    notify.assert_called_once()
    assert "nope" in notify.call_args[0][1]
    popen.assert_not_called()


def test_open_dashboard_launches_when_ready(tray):
    with patch.object(tray, "hud_readiness", return_value=None), patch.object(
        sonar_tray.subprocess, "Popen"
    ) as popen:
        tray.open_dashboard()
    popen.assert_called_once()
    argv = popen.call_args[0][0]
    assert argv[0] == sys.executable and argv[1].endswith("dashboard.py")
