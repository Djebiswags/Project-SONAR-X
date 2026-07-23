import unittest
from unittest.mock import patch, MagicMock

# Import dashboard
import dashboard

class TestSonarHUD(unittest.TestCase):
    @patch('psutil.cpu_percent', return_value=12.5)
    @patch('psutil.virtual_memory')
    def test_dashboard_creation_and_update(self, mock_virtual_memory, mock_cpu_percent):
        # Mock virtual memory percent
        mock_mem = MagicMock()
        mock_mem.percent = 45.0
        mock_virtual_memory.return_value = mock_mem

        # Instantiate SonarHUD
        hud = dashboard.create_dashboard()

        # Verify initial config and layout
        self.assertIsNotNone(hud._update_job)
        self.assertIn("🟢 CPU Load: 12.5%", hud.cpu_label.cget("text"))
        self.assertIn("🟢 RAM Usage: 45.0%", hud.ram_label.cget("text"))

        # Test state when CPU and RAM are high
        mock_cpu_percent.return_value = 85.0
        mock_mem.percent = 90.0

        # Call update_telemetry directly to simulate next iteration
        hud.update_telemetry()
        self.assertIn("🚨 CPU Load: 85.0%", hud.cpu_label.cget("text"))
        self.assertIn("🚨 RAM Usage: 90.0%", hud.ram_label.cget("text"))

        # Safely destroy the HUD
        hud.destroy()
        self.assertIsNone(hud._update_job)

if __name__ == "__main__":
    unittest.main()
