import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_dashboard_creation_and_telemetry(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 45.0
        mock_ram.return_value.percent = 60.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🟢 45.0%", hud.cpu_label.cget("text"))
        self.assertIn("60.0%", hud.ram_label.cget("text"))
        self.assertIsNotNone(hud._timer_id)

        hud.destroy()
        self.assertIsNone(hud._timer_id)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_dashboard_alert_icon(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 85.0
        mock_ram.return_value.percent = 70.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🚨 85.0%", hud.cpu_label.cget("text"))

        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_escape_key_closes_hud(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        # After Escape, destroy should have been called and timer cleared
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
