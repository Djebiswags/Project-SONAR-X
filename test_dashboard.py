import unittest
import tkinter as tk
from unittest.mock import patch
from dashboard import create_dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_initialization_and_normal_telemetry(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 45.0
        mock_ram.return_value.percent = 50.0

        hud = create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")
            self.assertIn("🟢", cpu_text)
            self.assertIn("45.0%", cpu_text)
            self.assertIn("50.0%", ram_text)
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_alert_telemetry(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 85.0
        mock_ram.return_value.percent = 90.0

        hud = create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")
            self.assertIn("🚨", cpu_text)
            self.assertIn("85.0%", cpu_text)
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_escape_key_closes_window(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Trigger Escape key event
        hud.event_generate("<Escape>")

        try:
            exists = hud.winfo_exists()
        except tk.TclError:
            exists = 0

        self.assertEqual(exists, 0)


if __name__ == "__main__":
    unittest.main()
