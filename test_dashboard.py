import unittest
from unittest.mock import patch

from dashboard import create_dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_update_telemetry_normal(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value.percent = 40.0

        hud = create_dashboard()
        self.addCleanup(hud.destroy)

        self.assertIn("🟢 CPU Load: 25.0%", hud.cpu_label.cget("text"))
        self.assertIn("🟢 RAM Usage: 40.0%", hud.ram_label.cget("text"))

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_update_telemetry_high_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 92.5
        mock_ram.return_value.percent = 88.0

        hud = create_dashboard()
        self.addCleanup(hud.destroy)

        self.assertIn("🚨 CPU Load: 92.5%", hud.cpu_label.cget("text"))
        self.assertIn("🚨 RAM Usage: 88.0%", hud.ram_label.cget("text"))

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_escape_key_closes_window(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        with self.assertRaises(Exception):
            hud.winfo_exists()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_destroy_cleanup(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = create_dashboard()
        self.assertIsNotNone(hud._after_job)

        hud.destroy()
        self.assertIsNone(hud._after_job)


if __name__ == "__main__":
    unittest.main()
