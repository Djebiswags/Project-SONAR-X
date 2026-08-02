import unittest
from unittest.mock import MagicMock, patch
from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        # We need a display to initialize Tkinter/CustomTkinter widgets.
        # This test should be run under xvfb-run in headless environments.
        self.hud = create_dashboard()

    def tearDown(self):
        try:
            self.hud.destroy()
        except Exception:
            pass

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_multimodal_telemetry_normal(self, mock_virtual_memory, mock_cpu_percent):
        # Set normal load values
        mock_cpu_percent.return_value = 45.0

        mock_ram = MagicMock()
        mock_ram.percent = 50.0
        mock_virtual_memory.return_value = mock_ram

        # Call update_telemetry to apply the mock values
        self.hud.update_telemetry()

        # Check normal telemetry labels (should have 🟢)
        self.assertIn("🟢 CPU Load: 45.0%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("🟢 RAM Usage: 50.0%", self.hud.ram_label.cget("text"))

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_multimodal_telemetry_high(self, mock_virtual_memory, mock_cpu_percent):
        # Set high load values
        mock_cpu_percent.return_value = 85.0

        mock_ram = MagicMock()
        mock_ram.percent = 90.0
        mock_virtual_memory.return_value = mock_ram

        # Call update_telemetry to apply the mock values
        self.hud.update_telemetry()

        # Check high telemetry labels (should have 🚨 and red color for CPU)
        self.assertIn("🚨 CPU Load: 85.0%", self.hud.cpu_label.cget("text"))
        self.assertEqual(self.hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertIn("🚨 RAM Usage: 90.0%", self.hud.ram_label.cget("text"))

    def test_teardown_cancels_job(self):
        # Store initial job ID
        job_id = self.hud._telemetry_job
        self.assertIsNotNone(job_id, "Telemetry update job should be scheduled.")

        # Spy on after_cancel to ensure it gets called on destroy
        self.hud.after_cancel = MagicMock(side_effect=self.hud.after_cancel)
        self.hud.destroy()

        # Verify that after_cancel was called with our job ID
        self.hud.after_cancel.assert_called_once_with(job_id)
        self.assertIsNone(self.hud._telemetry_job, "Telemetry job ID should be cleared after destroy.")

    def test_escape_key_closes_hud(self):
        # Force window focus and update window tasks
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

        # Mock the destroy method to check if Escape triggers it
        self.hud.destroy = MagicMock(side_effect=self.hud.destroy)

        # Generate a simulated Escape key press
        self.hud.event_generate("<Escape>")
        self.hud.update()

        # Assert destroy was called upon receiving Escape key event
        self.hud.destroy.assert_called_once()


if __name__ == "__main__":
    unittest.main()
