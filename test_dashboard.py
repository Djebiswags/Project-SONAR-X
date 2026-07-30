import unittest
from unittest.mock import patch, MagicMock

# Make sure we can run with xvfb-run
class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need an X display for Tkinter tests (like xvfb)
        cls.has_tkinter = False
        try:
            import tkinter  # noqa: F401
            import customtkinter  # noqa: F401
            cls.has_tkinter = True
        except ImportError:
            pass

    def setUp(self):
        if not self.has_tkinter:
            self.skipTest("Tkinter or CustomTkinter not available in this environment.")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        # Let some events process
        hud.update_idletasks()
        hud.update()

        # Check texts and colors
        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 45.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 60.0%")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_alert_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        hud.update_idletasks()
        hud.update()

        # Check alert state
        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 85.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_memory.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        # Force focus and deiconify
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Verify it has not been destroyed yet
        self.assertIsNotNone(hud._update_job)

        # Generate global Escape key press event
        hud.event_generate("<Escape>")
        hud.update()

        # Check that it's destroyed (checking if _update_job gets cleared and window is gone)
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
