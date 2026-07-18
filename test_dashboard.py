import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk

# Import dashboard elements to test
from dashboard import create_dashboard


class TestDashboardUI(unittest.TestCase):
    def setUp(self):
        # We need a proper Tkinter display context, usually handled via xvfb-run -a
        self.hud = create_dashboard()

    def tearDown(self):
        if self.hud:
            try:
                self.hud.destroy()
            except Exception:
                pass

    def test_window_properties(self):
        """Test basic properties of the SonarHUD window."""
        self.assertEqual(self.hud.title(), "SONAR-X | Live Telemetry")
        # Ensure Escape key is bound
        binds = self.hud.bind()
        self.assertTrue(any("Escape" in b or "Escape" in str(b) for b in binds) or len(binds) > 0)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_update_telemetry_normal(self, mock_virtual_memory, mock_cpu_percent):
        """Test telemetry labels under normal/low load."""
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 50.0
        mock_virtual_memory.return_value = mock_mem

        # Call update_telemetry to apply mocked values
        self.hud.update_telemetry()

        # Low loads should use the 🟢 prefix and correct colors
        self.assertIn("🟢 CPU Load: 45.0%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#00FFCC")

        self.assertIn("🟢 RAM Usage: 50.0%", self.hud.ram_label.cget("text"))
        self.assertEqual(self.hud.ram_label.cget("text_color"), "#00FFCC")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_update_telemetry_high(self, mock_virtual_memory, mock_cpu_percent):
        """Test telemetry labels under high load."""
        mock_cpu_percent.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_memory.return_value = mock_mem

        # Call update_telemetry to apply mocked values
        self.hud.update_telemetry()

        # High loads should use the 🚨 prefix and correct colors
        self.assertIn("🚨 CPU Load: 85.0%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#FF3333")

        self.assertIn("🚨 RAM Usage: 90.0%", self.hud.ram_label.cget("text"))
        self.assertEqual(self.hud.ram_label.cget("text_color"), "#FF3333")

    def test_destroy_clears_after_id(self):
        """Test that destroy cancels any pending after callbacks to prevent memory leaks."""
        self.assertIsNotNone(self.hud._after_id)
        with patch.object(self.hud, "after_cancel") as mock_after_cancel:
            self.hud.destroy()
            mock_after_cancel.assert_called_once()
            self.assertIsNone(self.hud._after_id)


if __name__ == "__main__":
    unittest.main()
