import unittest
from unittest.mock import patch
import psutil
import customtkinter as ctk

class TestSonarDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry_stable(self, mock_virtual_mem, mock_cpu_percent):
        # Mock values: stable CPU (<= 80)
        mock_cpu_percent.return_value = 45.0
        mock_virtual_mem.return_value.percent = 60.0

        import dashboard
        hud = dashboard.create_dashboard()

        # Check titles, geometry
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")
        # Attributes can return 0 or 1 depending on OS/WM under X11
        self.assertIn(hud.attributes("-topmost"), (0, 1))

        # Verify CPU label starts with stable indicator 🟢 and correct load
        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 45.0%")
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 60.0%")

        # Verify Escape binding is registered
        self.assertTrue(hud.bind("<Escape>"))

        # Clean up window
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_telemetry_high_cpu(self, mock_virtual_mem, mock_cpu_percent):
        # Mock values: high CPU (> 80)
        mock_cpu_percent.return_value = 88.5
        mock_virtual_mem.return_value.percent = 70.0

        import dashboard
        hud = dashboard.create_dashboard()

        # Verify CPU label starts with warning indicator 🚨 and correct load
        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 88.5%")
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 70.0%")

        # Clean up window
        hud.destroy()


if __name__ == "__main__":
    unittest.main()
