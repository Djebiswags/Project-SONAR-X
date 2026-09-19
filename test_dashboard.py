import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 45.0
        hud = dashboard.create_dashboard()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("15.0%", cpu_text)
        self.assertIn("🟢", cpu_text)
        self.assertIn("45.0%", ram_text)
        self.assertIn("🟢", ram_text)

        hud.destroy()
        self.assertIsNone(hud._timer_id)

    @patch("psutil.cpu_percent", return_value=90.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_warning_indicators(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 85.0
        hud = dashboard.create_dashboard()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("🚨", cpu_text)
        self.assertIn("🚨", ram_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_dashboard_escape_key_closes_window(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        # Check that destroy was executed and window is no longer active / destroyed
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
