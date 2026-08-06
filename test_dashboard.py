import unittest
from unittest.mock import patch, MagicMock

# Import dashboard
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_create_dashboard_updates_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mocks
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard app instance
        hud = dashboard.create_dashboard()

        # Let's verify that the UI labels are created and updated correctly
        self.assertIn("🟢 CPU Load: 45.0%", hud.cpu_label.cget("text"))
        self.assertIn("🟢 RAM Usage: 60.0%", hud.ram_label.cget("text"))
        self.assertIsNotNone(hud._update_job)

        # Teardown the app
        hud.destroy()
        self.assertIsNone(hud._update_job)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_alert_states(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mock for alert threshold states
        mock_cpu_percent.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard app instance
        hud = dashboard.create_dashboard()

        # Verify that warning indicators are shown
        self.assertIn("🚨 CPU Load: 85.0%", hud.cpu_label.cget("text"))
        self.assertIn("🚨 RAM Usage: 90.0%", hud.ram_label.cget("text"))

        # Teardown the app
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mocks
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard and verify Escape key is bound globally
        hud = dashboard.create_dashboard()

        # Bring it to focus/display for simulation
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate the Escape key event programmatically
        hud.event_generate("<Escape>")
        hud.update()

        # The window should be destroyed, and _update_job should be cleared
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
