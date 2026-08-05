import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add directory to sys.path to find dashboard.py
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need customtkinter, let's mock psutil and verify imports
        import customtkinter as ctk
        cls.ctk = ctk

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_dashboard_creation_and_telemetry(self, mock_virtual_mem, mock_cpu):
        # Setup mocks
        mock_cpu.return_value = 15.0
        mock_mem = MagicMock()
        mock_mem.percent = 45.0
        mock_virtual_mem.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        try:
            # Verify initial widgets configuration under normal load
            cpu_text = hud.cpu_label.cget("text")
            self.assertIn("🟢", cpu_text)
            self.assertIn("15.0%", cpu_text)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

            # Verify RAM text
            ram_text = hud.ram_label.cget("text")
            self.assertIn("45.0%", ram_text)

            # Test high load triggers warning/emoji change
            mock_cpu.return_value = 85.0
            hud.update_telemetry()
            cpu_text_high = hud.cpu_label.cget("text")
            self.assertIn("🚨", cpu_text_high)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        finally:
            hud.destroy()

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_after_cancel_on_destroy(self, mock_virtual_mem, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 20.0
        mock_virtual_mem.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        # Check job ID is stored
        self.assertIsNotNone(hud._update_job_id)
        job_id = hud._update_job_id

        with patch.object(hud, 'after_cancel') as mock_cancel:
            hud.destroy()
            mock_cancel.assert_called_once_with(job_id)
            self.assertIsNone(hud._update_job_id)

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_escape_key_closes_window(self, mock_virtual_mem, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 20.0
        mock_virtual_mem.return_value = mock_mem

        from dashboard import create_dashboard
        hud = create_dashboard()

        # Let's ensure Tk has processed geometry/visibility
        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroyed = False
        original_destroy = hud.destroy
        def mock_destroy():
            nonlocal destroyed
            destroyed = True
            original_destroy()

        hud.destroy = mock_destroy

        # Generate Escape key event
        hud.event_generate('<Escape>')
        hud.update()

        self.assertTrue(destroyed)

if __name__ == '__main__':
    unittest.main()
