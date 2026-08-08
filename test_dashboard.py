import unittest
from unittest.mock import patch, MagicMock
from dashboard import create_dashboard


class TestSonarDashboard(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_dashboard_initialization_and_emojis_low(
        self, mock_virtual_mem, mock_cpu_percent
    ):
        # Configure mock values below 80%
        mock_cpu_percent.return_value = 45.5
        mock_mem = MagicMock()
        mock_mem.percent = 60.2
        mock_virtual_mem.return_value = mock_mem

        # Create the dashboard HUD
        hud = create_dashboard()
        try:
            # Let's force an update to process tkinter tasks
            hud.update()

            # Verify that labels are updated with correct low/normal state emojis and colors
            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            ram_color = hud.ram_label.cget("text_color")

            self.assertIn("🟢", cpu_text)
            self.assertIn("45.5%", cpu_text)
            self.assertEqual(cpu_color, "#00FFCC")

            self.assertIn("🟢", ram_text)
            self.assertIn("60.2%", ram_text)
            self.assertEqual(ram_color, "#00FFCC")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_dashboard_emojis_high(self, mock_virtual_mem, mock_cpu_percent):
        # Configure mock values above 80%
        mock_cpu_percent.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_mem.return_value = mock_mem

        # Create the dashboard HUD
        hud = create_dashboard()
        try:
            hud.update()

            # Verify labels are updated with alert emojis and red color
            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            ram_color = hud.ram_label.cget("text_color")

            self.assertIn("🚨", cpu_text)
            self.assertIn("85.0%", cpu_text)
            self.assertEqual(cpu_color, "#FF3333")

            self.assertIn("🚨", ram_text)
            self.assertIn("90.0%", ram_text)
            self.assertEqual(ram_color, "#FF3333")
        finally:
            hud.destroy()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_destroys_window(self, mock_virtual_mem, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_mem.return_value = mock_mem

        hud = create_dashboard()

        # Follow guidelines for testing keyboard events in Xvfb
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Monitor if destroy was called or if window is destroyed
        destroyed = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroyed
            destroyed = True
            original_destroy()

        hud.destroy = mock_destroy

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(
            destroyed, "The window should be destroyed when Escape is pressed."
        )

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    @patch("customtkinter.CTk.after_cancel")
    def test_destroy_cancels_after_job(
        self, mock_after_cancel, mock_virtual_mem, mock_cpu_percent
    ):
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_mem.return_value = mock_mem

        hud = create_dashboard()
        self.assertIsNotNone(hud._update_job, "Should schedule an after job on init")

        job_id = hud._update_job
        hud.destroy()

        mock_after_cancel.assert_called_once_with(job_id)
        self.assertIsNone(hud._update_job, "Should clear the job ID after cancel")


if __name__ == "__main__":
    unittest.main()
