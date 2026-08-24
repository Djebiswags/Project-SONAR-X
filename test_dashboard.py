import unittest
from unittest.mock import patch
import _tkinter
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=25.0)
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_normal_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        hud.update()

        label_text = hud.cpu_label.cget("text")
        self.assertIn("🟢", label_text)
        self.assertIn("25.0%", label_text)
        self.assertIsNotNone(hud._timer_id)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=85.0)
    @patch("psutil.virtual_memory")
    def test_hud_high_cpu_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        hud.update()

        label_text = hud.cpu_label.cget("text")
        self.assertIn("🚨", label_text)
        self.assertIn("85.0%", label_text)

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

        try:
            exists = bool(hud.winfo_exists())
        except _tkinter.TclError:
            exists = False

        self.assertFalse(exists)

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.update()

        timer_id = hud._timer_id
        self.assertIsNotNone(timer_id)

        hud.destroy()
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
