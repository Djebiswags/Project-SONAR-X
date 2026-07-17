import unittest
from unittest.mock import patch, MagicMock
import sys
import tkinter as tk

# Mocking modules and functions that might not be fully functional or have specific requirements
# in a headless CLI environment or without real system info.
sys.modules['rumps'] = MagicMock()

import dashboard

class TestDashboard(unittest.TestCase):
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_dashboard_creation_and_update(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mock behavior
        mock_cpu_percent.return_value = 15.0
        mock_mem = MagicMock()
        mock_mem.percent = 40.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard app instance
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Force geometry/update to test widget setup
        hud.update_idletasks()

        # Check default label updates
        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("15.0%", cpu_text)
        self.assertIn("🟢", cpu_text)
        self.assertIn("40.0%", ram_text)
        self.assertIn("🟢", ram_text)

        # Trigger update_telemetry with warning levels
        mock_cpu_percent.return_value = 85.0
        mock_mem.percent = 90.0

        hud.update_telemetry()

        cpu_text_warn = hud.cpu_label.cget("text")
        ram_text_warn = hud.ram_label.cget("text")

        self.assertIn("85.0%", cpu_text_warn)
        self.assertIn("🚨", cpu_text_warn)
        self.assertIn("90.0%", ram_text_warn)
        self.assertIn("🚨", ram_text_warn)

        # Ensure after_id is stored
        self.assertIsNotNone(hud._after_id)

        # Test destroy/after_cancel
        hud.destroy()
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
