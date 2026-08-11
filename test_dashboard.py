import unittest
from unittest.mock import patch, MagicMock

# Ensure we have tkinter/customtkinter available and can import and test
try:
    import customtkinter as ctk
except ImportError:
    ctk = None

import dashboard

class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if ctk is None:
            raise unittest.SkipTest("customtkinter is not available, skipping UI tests.")

    @patch("dashboard.psutil")
    def test_initialization_and_telemetry(self, mock_psutil):
        # Mock cpu_percent and virtual_memory
        mock_psutil.cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 50.0
        mock_psutil.virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()

        # Verify title and initial components
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Manually update telemetry to run through our emoji and color logic
        hud.update_telemetry()

        # Check text labels
        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("45.0%", cpu_text)
        self.assertIn("🟢", cpu_text)
        self.assertIn("50.0%", ram_text)
        self.assertIn("🟢", ram_text)

        # Now mock a high load scenario
        mock_psutil.cpu_percent.return_value = 90.0
        mock_mem.percent = 85.0

        hud.update_telemetry()

        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("90.0%", cpu_text)
        self.assertIn("🚨", cpu_text)
        self.assertIn("85.0%", ram_text)
        self.assertIn("🚨", ram_text)

        # Clean up
        hud.destroy()

    @patch("dashboard.psutil")
    def test_keyboard_escape_closes_hud(self, mock_psutil):
        # Mock psutil calls to prevent unnecessary background CPU usage during testing
        mock_psutil.cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_psutil.virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()

        # Ensure HUD is focused and updated so events are processed correctly
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate escape key event
        hud.event_generate("<Escape>")
        hud.update()

        # When hud is destroyed, its state should reflect that or _after_id is canceled/None
        self.assertIsNone(hud._after_id)

    @patch("dashboard.psutil")
    def test_destroy_cancels_scheduled_update(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_psutil.virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()

        self.assertIsNotNone(hud._after_id)

        # Destroy should cancel the update and clear the ID
        hud.destroy()
        self.assertIsNone(hud._after_id)

if __name__ == "__main__":
    unittest.main()
