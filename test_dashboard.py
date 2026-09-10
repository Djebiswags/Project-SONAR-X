import unittest
from unittest.mock import patch
import tkinter as tk
import dashboard


class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        self.hud = dashboard.create_dashboard()
        self.hud.deiconify()
        self.hud.update()

    def tearDown(self):
        try:
            if self.hud.winfo_exists():
                self.hud.destroy()
        except tk.TclError:
            pass

    def test_hud_initialization(self):
        self.assertEqual(self.hud.title(), "SONAR-X | Live Telemetry")
        self.assertIsNotNone(self.hud.cpu_label)
        self.assertIsNotNone(self.hud.ram_label)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_normal_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 45.0
        mock_ram.return_value.percent = 50.0

        self.hud.update_telemetry()

        self.assertIn("🟢 CPU Load: 45.0%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("RAM Usage: 50.0%", self.hud.ram_label.cget("text"))

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 88.5
        mock_ram.return_value.percent = 70.0

        self.hud.update_telemetry()

        self.assertIn("🚨 CPU Load: 88.5%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#FF3333")

    def test_escape_key_closes_hud(self):
        self.hud.focus_force()
        self.hud.update()
        self.hud.event_generate("<Escape>")
        self.hud.update()
        try:
            exists = self.hud.winfo_exists()
        except tk.TclError:
            exists = 0
        self.assertEqual(exists, 0)

    def test_destroy_cancels_timer(self):
        self.assertIsNotNone(self.hud._timer_id)
        self.hud.destroy()
        self.assertIsNone(self.hud._timer_id)


if __name__ == "__main__":
    unittest.main()
