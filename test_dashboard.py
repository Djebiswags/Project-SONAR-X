import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_telemetry_normal(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_ram.return_value.percent = 40.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🟢 15.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("40.0%", hud.ram_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_telemetry_high_cpu(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 92.5
        mock_ram.return_value.percent = 75.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🚨 92.5%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_closes_window(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 30.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        # Check that after_id is reset and window destroy cleanup occurs
        self.assertIsNone(hud._after_id)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_destroy_cancels_after_timer(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 30.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIsNotNone(hud._after_id)
        hud.destroy()
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
