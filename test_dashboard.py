import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import _tkinter

# Add current directory to path if needed
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dashboard import create_dashboard

class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        # We patch psutil within create_dashboard / update_telemetry to avoid real system readings
        self.cpu_patcher = patch("psutil.cpu_percent")
        self.ram_patcher = patch("psutil.virtual_memory")

        self.mock_cpu = self.cpu_patcher.start()
        self.mock_ram = self.ram_patcher.start()

        # Default mock values
        self.mock_cpu.return_value = 10.0

        mock_mem = MagicMock()
        mock_mem.percent = 40.0
        self.mock_ram.return_value = mock_mem

        # Instantiate the dashboard
        self.hud = create_dashboard()

    def tearDown(self):
        # Clean up any remaining tk window to prevent leaks
        try:
            self.hud.destroy()
        except Exception:
            pass
        self.cpu_patcher.stop()
        self.ram_patcher.stop()

    def test_hud_initialization(self):
        """Test that HUD and its widgets are correctly initialized with default states."""
        self.assertEqual(self.hud.title(), "SONAR-X | Live Telemetry")

        # Verify initial label texts containing healthy emojis
        self.assertIn("🟢", self.hud.cpu_label.cget("text"))
        self.assertIn("🟢", self.hud.ram_label.cget("text"))

    def test_escape_key_closes_hud(self):
        """Test that pressing Escape key destroys/closes the HUD window."""
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

        # Generate Escape key event
        self.hud.event_generate("<Escape>")
        self.hud.update()

        # Verify that the HUD window has been destroyed
        try:
            exists = self.hud.winfo_exists()
        except _tkinter.TclError:
            exists = False
        self.assertFalse(exists)

    def test_telemetry_high_thresholds(self):
        """Test that warning emojis (🚨) are displayed when values cross 80%."""
        # Setup mock returns for high load
        self.mock_cpu.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        self.mock_ram.return_value = mock_mem

        # Trigger update manually to test immediate effect
        self.hud.update_telemetry()

        # Verify that labels are updated with the alert emojis
        self.assertIn("🚨", self.hud.cpu_label.cget("text"))
        self.assertIn("🚨", self.hud.ram_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertEqual(self.hud.ram_label.cget("text_color"), "#FF3333")

    def test_telemetry_low_thresholds(self):
        """Test that healthy emojis (🟢) are displayed when values are 80% or less."""
        self.mock_cpu.return_value = 50.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        self.mock_ram.return_value = mock_mem

        self.hud.update_telemetry()

        self.assertIn("🟢", self.hud.cpu_label.cget("text"))
        self.assertIn("🟢", self.hud.ram_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(self.hud.ram_label.cget("text_color"), "#00FFCC")


if __name__ == "__main__":
    unittest.main()
