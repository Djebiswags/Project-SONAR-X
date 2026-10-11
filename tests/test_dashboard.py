from unittest.mock import patch

import pytest

ctk = pytest.importorskip("customtkinter")
pytest.importorskip("tkinter")

import dashboard


def test_dashboard_creation_and_telemetry_normal(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 42.0)
    monkeypatch.setattr(
        "psutil.virtual_memory",
        lambda: type("RAM", (), {"percent": 55.0})(),
    )

    hud = dashboard.create_dashboard()
    try:
        hud.update()
        assert "🟢 CPU Load: 42.0%" in hud.cpu_label.cget("text")
        assert "RAM Usage: 55.0%" in hud.ram_label.cget("text")
        assert hud._timer_id is not None
    finally:
        hud.destroy()


def test_dashboard_telemetry_high_cpu(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 88.5)
    monkeypatch.setattr(
        "psutil.virtual_memory",
        lambda: type("RAM", (), {"percent": 70.0})(),
    )

    hud = dashboard.create_dashboard()
    try:
        hud.update()
        assert "🚨 CPU Load: 88.5%" in hud.cpu_label.cget("text")
    finally:
        hud.destroy()


def test_dashboard_escape_key_closes_hud(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 30.0)
    monkeypatch.setattr(
        "psutil.virtual_memory",
        lambda: type("RAM", (), {"percent": 40.0})(),
    )

    hud = dashboard.create_dashboard()
    hud.deiconify()
    hud.focus_force()
    hud.update()

    destroyed = False

    original_destroy = hud.destroy

    def mock_destroy():
        nonlocal destroyed
        destroyed = True
        original_destroy()

    hud.destroy = mock_destroy

    hud.event_generate("<Escape>")
    hud.update()

    assert destroyed is True


def test_dashboard_destroy_cancels_timer(monkeypatch):
    monkeypatch.setattr("psutil.cpu_percent", lambda: 20.0)
    monkeypatch.setattr(
        "psutil.virtual_memory",
        lambda: type("RAM", (), {"percent": 30.0})(),
    )

    hud = dashboard.create_dashboard()
    timer_id = hud._timer_id
    assert timer_id is not None

    with patch.object(hud, "after_cancel") as mock_cancel:
        hud.destroy()
        mock_cancel.assert_called_with(timer_id)

    assert hud._timer_id is None
