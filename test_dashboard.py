import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
import dashboard


class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need a Tkinter/ctk app initialized for testing widget bindings and properties.
        # This will run inside xvfb-run on headless systems.
        ctk.set_appearance_mode("dark")

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_initialization_and_telemetry_low(self, mock_cpu, mock_ram):
        # Mock low CPU and RAM
        mock_cpu.return_value = 15.0
        mock_ram.return_value = MagicMock(percent=45.0)

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)

        # Verify initial telemetry updates with normal/low stats (green / emoji)
        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")

        self.assertIn("🟢 CPU Load: 15.0%", cpu_text)
        self.assertEqual(cpu_color, "#00FFCC")
        self.assertIn("💾 RAM Usage: 45.0%", ram_text)
        self.assertEqual(ram_color, "#FFFFFF")

        # Cleanup
        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_telemetry_high(self, mock_cpu, mock_ram):
        # Mock high CPU and RAM
        mock_cpu.return_value = 85.0
        mock_ram.return_value = MagicMock(percent=92.0)

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)

        # Trigger telemetry update
        hud.update_telemetry()

        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")

        self.assertIn("🚨 CPU Load: 85.0%", cpu_text)
        self.assertEqual(cpu_color, "#FF3333")
        self.assertIn("⚠️ RAM Usage: 92.0%", ram_text)
        self.assertEqual(ram_color, "#FF9900")

        # Cleanup
        hud.destroy()

    def test_escape_key_binding(self):
        hud = dashboard.create_dashboard()
        hud.focus_force()
        hud.update()

        # Verify binding exists on the class/instance level
        # We can simulate the Escape key event callback
        destroy_called = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroy_called
            destroy_called = True
            original_destroy()

        hud.destroy = mock_destroy

        # Generate an event structure or trigger directly
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroy_called)

    def test_after_cancel_on_destroy(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._after_id)

        after_id = hud._after_id

        with patch.object(hud, "after_cancel", wraps=hud.after_cancel) as mock_cancel:
            hud.destroy()
            mock_cancel.assert_called_once_with(after_id)
            self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
