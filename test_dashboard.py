import unittest
from unittest.mock import patch

import dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_hud_creation_and_telemetry_normal(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        try:
            self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")
            self.assertIn("🟢 CPU Load: 15.0%", hud.cpu_label.cget("text"))
            self.assertIn("RAM Usage: 40.0%", hud.ram_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
            self.assertIsNotNone(hud._timer)
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent", return_value=92.5)
    @patch("psutil.virtual_memory")
    def test_hud_telemetry_high_load(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 85.0
        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🚨 CPU Load: 92.5%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        timer_id = hud._timer
        self.assertIsNotNone(timer_id)

        with patch.object(hud, "after_cancel", wraps=hud.after_cancel) as mock_cancel:
            hud.destroy()
            mock_cancel.assert_called_once_with(timer_id)
            self.assertIsNone(hud._timer)

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroyed = []
        original_destroy = hud.destroy

        def mock_destroy():
            destroyed.append(True)
            original_destroy()

        hud.destroy = mock_destroy
        hud.event_generate("<Escape>")
        hud.update()
        self.assertTrue(destroyed, "Escape key event should trigger HUD destruction")


if __name__ == "__main__":
    unittest.main()
