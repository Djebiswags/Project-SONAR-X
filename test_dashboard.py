import unittest
from unittest.mock import patch
import dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_telemetry_normal(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 15.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 40.0%")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=92.5)
    @patch("psutil.virtual_memory")
    def test_telemetry_high_cpu_redline(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 75.0
        hud = dashboard.create_dashboard()
        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 92.5%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        hud.destroy()

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_dismisses_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroyed = False

        def mark_destroyed():
            nonlocal destroyed
            destroyed = True

        hud.bind("<Destroy>", lambda e: mark_destroyed() if e.widget == hud else None)
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroyed or not hud.winfo_exists())

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
