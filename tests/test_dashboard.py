from unittest.mock import patch

import pytest

ctk = pytest.importorskip("customtkinter")
dashboard = pytest.importorskip("dashboard")


def test_dashboard_creation_and_telemetry():
    with patch("psutil.cpu_percent", return_value=15.0), patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 45.0
        hud = dashboard.create_dashboard()
        hud.update()
        assert "🟢" in hud.cpu_label.cget("text")
        assert "15" in hud.cpu_label.cget("text")
        assert "45" in hud.ram_label.cget("text")
        hud.destroy()


def test_dashboard_high_cpu_indicator():
    with patch("psutil.cpu_percent", return_value=85.0), patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 60.0
        hud = dashboard.create_dashboard()
        hud.update()
        assert "🚨" in hud.cpu_label.cget("text")
        assert hud.cpu_label.cget("text_color") == "#FF3333"
        hud.destroy()


def test_dashboard_escape_key_closes():
    hud = dashboard.create_dashboard()
    hud.deiconify()
    hud.focus_force()
    hud.update()

    destroyed = False

    def on_destroy(event=None):
        nonlocal destroyed
        destroyed = True

    hud.bind("<Destroy>", on_destroy)
    hud.event_generate("<Escape>")
    hud.update()

    assert destroyed or not hud.winfo_exists()


def test_dashboard_destroy_teardown_cancels_job():
    hud = dashboard.create_dashboard()
    hud.update()
    assert hud._update_job is not None
    hud.destroy()
    assert hud._update_job is None
