import unittest
from unittest.mock import patch

import dashboard


class TestDashboard(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_creation_and_telemetry(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_vm.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._after_id)
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))

        # Test high load status indicator
        mock_cpu.return_value = 92.0
        hud.update_telemetry()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("92.0%", hud.cpu_label.cget("text"))

        # Clean destroy
        hud.destroy()
        self.assertIsNone(hud._after_id)

    @patch("dashboard.psutil.cpu_percent", return_value=10.0)
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Simulate Escape key press
        hud.event_generate("<Escape>")
        hud.update()
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
