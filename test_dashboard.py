import unittest
from unittest.mock import patch, MagicMock
import dashboard

class TestDashboard(unittest.TestCase):

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_dashboard_telemetry_updates_normal(self, mock_virtual_mem, mock_cpu):
        # Set up mocks
        mock_cpu.return_value = 15.0
        mock_mem = MagicMock()
        mock_mem.percent = 45.0
        mock_virtual_mem.return_value = mock_mem

        # Instantiate SonarHUD
        hud = dashboard.create_dashboard()

        # Update telemetry and check actual configuration values
        hud.update_telemetry()

        # Retrieve the text and text_color config using cget (customtkinter uses cget/configure)
        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 15.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "🟢 RAM Usage: 45.0%")
        self.assertEqual(hud.ram_label.cget("text_color"), "#00FFCC")
        hud.destroy()

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_dashboard_telemetry_updates_high_load(self, mock_virtual_mem, mock_cpu):
        # Set up high load mocks
        mock_cpu.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_mem.return_value = mock_mem

        hud = dashboard.create_dashboard()

        hud.update_telemetry()

        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 85.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertEqual(hud.ram_label.cget("text"), "🚨 RAM Usage: 90.0%")
        self.assertEqual(hud.ram_label.cget("text_color"), "#FF3333")
        hud.destroy()

    def test_destroy_cancels_job(self):
        hud = dashboard.create_dashboard()
        hud.telemetry_job = "after#1"

        # Mock after_cancel
        hud.after_cancel = MagicMock()

        # Call destroy and check job cancellation
        hud.destroy()
        hud.after_cancel.assert_called_once_with("after#1")
        self.assertIsNone(hud.telemetry_job)

if __name__ == "__main__":
    unittest.main()
