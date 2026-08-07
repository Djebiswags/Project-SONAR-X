import unittest
from unittest.mock import patch, MagicMock
from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_telemetry(self, mock_virtual_mem, mock_cpu):
        # Setup mocks
        mock_cpu.return_value = 15.5
        mock_mem = MagicMock()
        mock_mem.percent = 45.2
        mock_virtual_mem.return_value = mock_mem

        # Instantiate dashboard
        hud = create_dashboard()
        self.assertIsNotNone(hud)

        # Verify initial config and layout
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Force a rendering update to process the initial values
        hud.update_idletasks()

        # Check standard CPU output
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.5%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

        # Check standard RAM output
        self.assertIn("45.2%", hud.ram_label.cget("text"))

        # Test Redline behavior
        mock_cpu.return_value = 85.0
        hud.update_telemetry()

        # Check redline CPU output
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("85.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        # Clean teardown
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_binding(self, mock_virtual_mem, mock_cpu):
        # Setup mocks
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 40.0
        mock_virtual_mem.return_value = mock_mem

        # Instantiate dashboard
        hud = create_dashboard()

        # Make sure window is deiconified and focused
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Check that after_id is not None
        self.assertIsNotNone(hud._after_id)

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        # The hud should be destroyed and after_id should be cleared or window should not exist
        # We can test after_id is None after destroy, or that we overridden destroy correctly
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
