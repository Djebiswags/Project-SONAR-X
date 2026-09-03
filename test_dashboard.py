import unittest
from unittest.mock import patch
import dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=25.0)
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_multi_modal_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        hud.update()

        label_text = hud.cpu_label.cget("text")
        self.assertIn("🟢", label_text)
        self.assertIn("25.0%", label_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=92.0)
    @patch("psutil.virtual_memory")
    def test_hud_high_cpu_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        hud.update()

        label_text = hud.cpu_label.cget("text")
        self.assertIn("🚨", label_text)
        self.assertIn("92.0%", label_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_closes_window(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        # Check timer cancellation and destruction
        self.assertIsNone(hud._timer_job)

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_hud_destroy_cancels_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._timer_job)

        hud.destroy()
        self.assertIsNone(hud._timer_job)


if __name__ == "__main__":
    unittest.main()
