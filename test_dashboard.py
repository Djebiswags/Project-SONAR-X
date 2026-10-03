import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def test_create_dashboard_and_telemetry(self):
        with patch("psutil.cpu_percent", return_value=15.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 42.0
            hud = dashboard.create_dashboard()
            try:
                self.assertIn("🟢 CPU Load: 15.0%", hud.cpu_label.cget("text"))
                self.assertIn("RAM Usage: 42.0%", hud.ram_label.cget("text"))
            finally:
                hud.destroy()

    def test_high_cpu_indicator(self):
        with patch("psutil.cpu_percent", return_value=92.5), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 50.0
            hud = dashboard.create_dashboard()
            try:
                self.assertIn("🚨 CPU Load: 92.5%", hud.cpu_label.cget("text"))
            finally:
                hud.destroy()

    def test_escape_key_dismisses_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key event
        hud.event_generate("<Escape>")

        # Window was destroyed by Escape key handler
        with self.assertRaises(Exception):
            hud.winfo_exists()

    def test_destroy_cleans_up_timer(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._timer_id)
        hud.destroy()
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
