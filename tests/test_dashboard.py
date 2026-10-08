from unittest.mock import patch
import pytest

pytest.importorskip("tkinter")
pytest.importorskip("customtkinter")

from dashboard import create_dashboard


def test_dashboard_creation_and_telemetry():
    with patch("psutil.cpu_percent", return_value=15.0), \
         patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 45.0
        hud = create_dashboard()
        assert "🟢 CPU Load: 15.0%" in hud.cpu_label.cget("text")
        assert hud.cpu_label.cget("text_color") == "#00FFCC"
        assert "RAM Usage: 45.0%" in hud.ram_label.cget("text")
        hud.destroy()


def test_dashboard_high_cpu_alert():
    with patch("psutil.cpu_percent", return_value=92.0), \
         patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 80.0
        hud = create_dashboard()
        assert "🚨 CPU Load: 92.0%" in hud.cpu_label.cget("text")
        assert hud.cpu_label.cget("text_color") == "#FF3333"
        hud.destroy()


def test_dashboard_escape_key_closes_hud():
    with patch("psutil.cpu_percent", return_value=10.0), \
         patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 30.0
        hud = create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key press event
        hud.event_generate("<Escape>")

        # Checking winfo_exists or TclError when application is destroyed
        try:
            exists = hud.winfo_exists()
        except Exception:
            exists = False
        assert not exists


def test_dashboard_destroy_cancels_timer():
    with patch("psutil.cpu_percent", return_value=10.0), \
         patch("psutil.virtual_memory") as mock_ram:
        mock_ram.return_value.percent = 30.0
        hud = create_dashboard()
        assert hud._timer_id is not None
        hud.destroy()
        assert hud._timer_id is None
