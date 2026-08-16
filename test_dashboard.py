import unittest
from unittest.mock import patch
import dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent", return_value=15.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_normal_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 45.0
        hud = dashboard.create_dashboard()
        self.assertIn("🟢 CPU Load: 15.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 45.0%")
        self.assertIsNotNone(hud._timer_id)
        hud.destroy()
        self.assertIsNone(hud._timer_id)

    @patch("dashboard.psutil.cpu_percent", return_value=85.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_high_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 90.0
        hud = dashboard.create_dashboard()
        self.assertIn("🚨 CPU Load: 85.0%", hud.cpu_label.cget("text"))
        hud.destroy()

    @patch("dashboard.psutil.cpu_percent", return_value=10.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_escape_key_closes(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")
        hud.update()
        # After Escape, the window is destroyed
        with self.assertRaises(Exception):
            hud.winfo_exists()


if __name__ == "__main__":
    unittest.main()
