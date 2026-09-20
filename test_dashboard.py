import unittest
from unittest.mock import patch
import _tkinter
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_ram.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))
        self.assertIsNotNone(hud._update_job)

        hud.destroy()
        self.assertIsNone(hud._update_job)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_high_cpu_alert_icon(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 95.0
        mock_ram.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("95.0%", hud.cpu_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_dashboard(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_ram.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key event
        hud.event_generate("<Escape>")

        try:
            exists = bool(hud.winfo_exists())
        except _tkinter.TclError:
            exists = False

        self.assertFalse(exists)


if __name__ == "__main__":
    unittest.main()
