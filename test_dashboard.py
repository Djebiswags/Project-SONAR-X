import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_indicators_and_escape(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 45.0
        mock_vm.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.cpu_label.cget("text"))

        mock_cpu.return_value = 88.0
        hud.update_telemetry()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("88.0%", hud.cpu_label.cget("text"))

        # Test cleanup on destroy
        self.assertIsNotNone(hud._timer)
        hud.destroy()
        self.assertIsNone(hud._timer)


if __name__ == "__main__":
    unittest.main()
