import unittest
from unittest.mock import patch
import dashboard

class TestDashboardUX(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent", return_value=15.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_normal_cpu_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 45.0
        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🟢", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.cpu_percent", return_value=95.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_high_cpu_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🚨", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.cpu_percent", return_value=20.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_and_destroy_cleanup(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Verify job scheduled
        self.assertIsNotNone(hud._update_job)

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        # Job should be canceled and cleaned up
        self.assertIsNone(hud._update_job)

if __name__ == "__main__":
    unittest.main()
