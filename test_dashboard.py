import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_normal_status(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_ram.return_value.percent = 40.0

        hud = dashboard.create_dashboard()
        self.addCleanup(hud.destroy)

        hud.update_telemetry()
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("25.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_high_cpu_status(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 95.0
        mock_ram.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        self.addCleanup(hud.destroy)

        hud.update_telemetry()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("95.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_and_destroy_cleanup(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)

        # Trigger Escape key event using event_generate
        hud.deiconify()
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")

        # Check update job cleanup on destroy
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
