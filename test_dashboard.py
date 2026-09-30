import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent", return_value=15.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_create_dashboard_normal_status(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 45.0
        hud = dashboard.create_dashboard()
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("🟢", hud.ram_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))
        hud.destroy()
        hud.update()

    @patch("dashboard.psutil.cpu_percent", return_value=95.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_create_dashboard_high_load_status(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 88.0
        hud = dashboard.create_dashboard()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("95.0%", hud.cpu_label.cget("text"))
        self.assertIn("⚠️", hud.ram_label.cget("text"))
        self.assertIn("88.0%", hud.ram_label.cget("text"))
        hud.destroy()
        hud.update()

    @patch("dashboard.psutil.cpu_percent", return_value=10.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Simulate Escape key press
        hud.event_generate("<Escape>")
        hud.update()

        # Check that destroy cleaned up job ID
        self.assertIsNone(hud._update_job)

    @patch("dashboard.psutil.cpu_percent", return_value=10.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_destroy_cleans_up_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)
        hud.destroy()
        hud.update()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
