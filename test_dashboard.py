import unittest
from unittest.mock import patch

import dashboard


class TestDashboard(unittest.TestCase):
    @patch("dashboard.psutil")
    def test_dashboard_creation_and_telemetry(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = 12.5
        mock_psutil.virtual_memory.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        self.assertIn("12.5%", hud.cpu_label.cget("text"))
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))

        # Test high CPU state
        mock_psutil.cpu_percent.return_value = 85.0
        hud.update_telemetry()
        self.assertIn("85.0%", hud.cpu_label.cget("text"))
        self.assertIn("🚨", hud.cpu_label.cget("text"))

        # Verify timer cancellation on destroy
        after_id = hud._after_id
        self.assertIsNotNone(after_id)
        hud.destroy()
        self.assertIsNone(hud._after_id)

    @patch("dashboard.psutil")
    def test_escape_key_closes_hud(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = 10.0
        mock_psutil.virtual_memory.return_value.percent = 20.0

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

        self.assertTrue(destroyed, "Escape key should trigger window destruction")


if __name__ == "__main__":
    unittest.main()
