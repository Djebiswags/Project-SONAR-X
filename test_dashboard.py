import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 42.0
        hud = dashboard.create_dashboard()
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("42.0%", hud.ram_label.cget("text"))
        self.assertIsNotNone(hud._update_job)
        hud.destroy()
        self.assertIsNone(hud._update_job)

    @patch("psutil.cpu_percent", return_value=95.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_alert_icon(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 85.0
        hud = dashboard.create_dashboard()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("95.0%", hud.cpu_label.cget("text"))
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")
        hud.update()
        with self.assertRaises(Exception):
            hud.winfo_exists()


if __name__ == "__main__":
    unittest.main()
