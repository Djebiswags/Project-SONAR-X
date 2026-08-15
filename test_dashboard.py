import unittest
from unittest.mock import patch
import dashboard


class TestDashboardUX(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_telemetry_labels_normal_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")
            self.assertIn("🟢", cpu_text)
            self.assertIn("25.0%", cpu_text)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_telemetry_labels_high_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 85.0
        mock_ram.return_value.percent = 70.0

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")
            self.assertIn("🚨", cpu_text)
            self.assertIn("85.0%", cpu_text)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_escape_key_and_destroy_cleanup(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        self.assertIsNotNone(hud._after_id)

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        # Check that destroy cleaned up after_id
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
