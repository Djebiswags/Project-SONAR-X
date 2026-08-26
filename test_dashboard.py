import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=45.0)
    @patch("psutil.virtual_memory")
    def test_telemetry_normal_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🟢 CPU Load: 45.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 30.0%")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=92.5)
    @patch("psutil.virtual_memory")
    def test_telemetry_redline_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 75.0
        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🚨 CPU Load: 92.5%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_dismissal(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        self.assertIsNone(hud.timer_id)

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_destroy_timer_cleanup(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.update()

        timer_id = hud.timer_id
        self.assertIsNotNone(timer_id)

        hud.destroy()
        self.assertIsNone(hud.timer_id)


if __name__ == "__main__":
    unittest.main()
