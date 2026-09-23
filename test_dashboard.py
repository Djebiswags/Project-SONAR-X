import unittest
from unittest.mock import patch
import dashboard


class TestDashboardAccessibility(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_status_indicators(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 45.0

        # Normal CPU load (< 80)
        mock_cpu.return_value = 25.0
        hud = dashboard.create_dashboard()
        hud.update()
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("25.0%", hud.cpu_label.cget("text"))

        # High CPU load (> 80)
        mock_cpu.return_value = 88.0
        hud.update_telemetry()
        hud.update()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("88.0%", hud.cpu_label.cget("text"))

        hud.destroy()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        mock_cpu.return_value = 10.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Simulate Escape key press
        hud.event_generate("<Escape>")
        hud.update()

        # Window state should be destroyed
        try:
            exists = bool(hud.winfo_exists())
        except Exception:
            exists = False
        self.assertFalse(exists)

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_teardown_cleans_timer(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        mock_cpu.return_value = 15.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIsNotNone(hud._timer_id)
        hud.destroy()
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
