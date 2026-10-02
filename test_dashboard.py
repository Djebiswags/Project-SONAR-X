import unittest
from unittest.mock import patch
import dashboard


class TestDashboardHUD(unittest.TestCase):
    def test_hud_creation(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)
        self.assertIn("SONAR-X", hud.title())
        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_normal_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 42.0
        mock_ram.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        hud.update_telemetry()

        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")

        self.assertIn("🟢", cpu_text)
        self.assertIn("42.0%", cpu_text)
        self.assertEqual(cpu_color, "#00FFCC")

        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high_cpu_indicator(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 95.0
        mock_ram.return_value.percent = 70.0

        hud = dashboard.create_dashboard()
        hud.update_telemetry()

        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")

        self.assertIn("🚨", cpu_text)
        self.assertIn("95.0%", cpu_text)
        self.assertEqual(cpu_color, "#FF3333")

        hud.destroy()

    def test_escape_key_and_destroy_teardown(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        update_job = hud._update_job
        self.assertIsNotNone(update_job)

        # Trigger Escape key
        hud.event_generate("<Escape>")
        hud.update()

        # Check job cancellation and window destruction
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
