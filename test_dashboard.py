import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def test_create_dashboard(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)
        self.assertIn("SONAR-X", hud.title())
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_normal_cpu(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 45.0
        mock_vm.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        self.assertIn("🟢 45.0%", hud.cpu_label.cget("text"))
        self.assertIn("RAM Usage: 50.0%", hud.ram_label.cget("text"))
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_high_cpu(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 92.5
        mock_vm.return_value.percent = 60.0

        hud = dashboard.create_dashboard()
        self.assertIn("🚨 92.5%", hud.cpu_label.cget("text"))
        hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key event
        hud.event_generate("<Key-Escape>")

        # Check that the window is no longer active / exists
        with self.assertRaises(Exception):
            _ = hud.winfo_exists() and hud.state()

    def test_destroy_cancels_after_job(self):
        hud = dashboard.create_dashboard()
        job_id = hud._update_job
        self.assertIsNotNone(job_id)
        hud.destroy()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
