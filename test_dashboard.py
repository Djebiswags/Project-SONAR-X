import _tkinter
import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=45.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry_normal(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        self.assertIn("🟢 45.0%", hud.cpu_label.cget("text"))
        self.assertIn("💻 50.0%", hud.ram_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=92.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_telemetry_high_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 70.0
        hud = dashboard.create_dashboard()
        self.assertIn("🚨 92.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")

        self.assertIsNone(hud._update_job)
        with self.assertRaises(_tkinter.TclError):
            hud.winfo_exists()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_after_job(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)
        hud.destroy()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
