import unittest
from unittest.mock import patch
import tkinter
import dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_hud_normal_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("15.0%", cpu_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=90.0)
    @patch("psutil.virtual_memory")
    def test_hud_high_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 70.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("90.0%", cpu_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_closes(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape key event
        hud.event_generate("<Escape>")

        # Once destroyed, accessing winfo_exists raises TclError because the tk app is destroyed
        with self.assertRaises(tkinter.TclError):
            hud.winfo_exists()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_hud_destroy_cleans_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        self.assertIsNotNone(hud._timer_id)
        hud.destroy()
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
