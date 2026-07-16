import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
import dashboard

class TestSonarHUD(unittest.TestCase):
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_hud_initialization_and_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        # Set mock values
        mock_cpu_percent.return_value = 45.0

        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard instance
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)

        # Verify the title
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Verify text and color for CPU under 80% (should be 🟢 and #00FFCC)
        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        self.assertIn("🟢", cpu_text)
        self.assertIn("45", cpu_text)
        self.assertEqual(cpu_color, "#00FFCC")

        # Verify text and color for RAM under 80% (should be 🟢 and #00FFCC)
        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")
        self.assertIn("🟢", ram_text)
        self.assertIn("60", ram_text)
        self.assertEqual(ram_color, "#00FFCC")

        hud.destroy()

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_hud_critical_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        # Set mock values above 80%
        mock_cpu_percent.return_value = 92.0

        mock_mem = MagicMock()
        mock_mem.percent = 85.0
        mock_virtual_memory.return_value = mock_mem

        # Create dashboard instance
        hud = dashboard.create_dashboard()

        # Verify text and color for CPU above 80% (should be 🚨 and #FF3333)
        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        self.assertIn("🚨", cpu_text)
        self.assertIn("92", cpu_text)
        self.assertEqual(cpu_color, "#FF3333")

        # Verify text and color for RAM above 80% (should be 🚨 and #FF3333)
        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")
        self.assertIn("🚨", ram_text)
        self.assertIn("85", ram_text)
        self.assertEqual(ram_color, "#FF3333")

        hud.destroy()

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_hud_escape_key_binding(self, mock_virtual_memory, mock_cpu_percent):
        # Set mock values
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()

        is_destroyed = False
        original_destroy = hud.destroy
        def mock_destroy():
            nonlocal is_destroyed
            is_destroyed = True
            original_destroy()

        hud.destroy = mock_destroy

        hud.focus_force()
        hud.update()

        # Generate an Escape event
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(is_destroyed)

if __name__ == '__main__':
    unittest.main()
