import unittest
from unittest.mock import MagicMock, patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("dashboard.psutil.virtual_memory")
    @patch("dashboard.psutil.cpu_percent")
    def test_dashboard_telemetry_normal_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value = MagicMock(percent=40.0)

        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🟢 CPU Load: 25.0%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
            self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 40.0%")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.virtual_memory")
    @patch("dashboard.psutil.cpu_percent")
    def test_dashboard_telemetry_high_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 85.5
        mock_ram.return_value = MagicMock(percent=75.0)

        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🚨 CPU Load: 85.5%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.virtual_memory")
    @patch("dashboard.psutil.cpu_percent")
    def test_escape_key_closes_hud(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key press event
        hud.event_generate("<Escape>")
        hud.update()

        # Check that window update_job is cleared after destroy
        self.assertIsNone(hud._update_job)

    @patch("dashboard.psutil.virtual_memory")
    @patch("dashboard.psutil.cpu_percent")
    def test_destroy_cancels_after_job(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)

        hud.destroy()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
