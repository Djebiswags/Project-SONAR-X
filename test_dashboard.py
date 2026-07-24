import unittest
from unittest.mock import patch, MagicMock

# Since we don't have a direct test framework, we'll write a basic test for SonarHUD
class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to run with xvfb or headless if possible
        pass

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_initialization_and_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mocks
        mock_cpu_percent.return_value = 45.0
        mock_vm = MagicMock()
        mock_vm.percent = 55.0
        mock_virtual_memory.return_value = mock_vm

        # Import create_dashboard from dashboard
        from dashboard import create_dashboard
        hud = create_dashboard()

        self.assertIsNotNone(hud)
        # Check initial configuration or layout properties
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Verify bindings and after jobs are set up
        self.assertIsNotNone(hud._update_job)

        # Test escape key event closes the window (it calls destroy)
        # Let's mock destroy
        with patch.object(hud, 'destroy'):
            hud.event_generate("<Escape>")
            # Need to update idle tasks to handle event if needed or just trigger manually
            hud.update_idletasks()
            # Escape was bound to lambda _: self.destroy()
            # Let's invoke the handler directly or check bind details
            bindings = hud.bind("<Escape>")
            self.assertTrue(len(bindings) > 0)

        # Test update_telemetry with normal cpu/ram
        hud.update_telemetry()
        self.assertIn("🟢 CPU Load: 45.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("🟢 RAM Usage: 55.0%", hud.ram_label.cget("text"))
        self.assertEqual(hud.ram_label.cget("text_color"), "#00FFCC")

        # Test update_telemetry with redline cpu/ram (> 80)
        mock_cpu_percent.return_value = 85.0
        mock_vm.percent = 90.0
        hud.update_telemetry()
        self.assertIn("🚨 CPU Load: 85.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertIn("🚨 RAM Usage: 90.0%", hud.ram_label.cget("text"))
        self.assertEqual(hud.ram_label.cget("text_color"), "#FF3333")

        # Clean up
        hud.destroy()
        self.assertIsNone(hud._update_job)

if __name__ == "__main__":
    unittest.main()
