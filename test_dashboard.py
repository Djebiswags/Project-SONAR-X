import unittest
from unittest.mock import MagicMock, patch
import dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_normal(self, mock_virtual_memory, mock_cpu_percent):
        # Setup low/normal values
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()
        try:
            # Let the telemetry tick process
            hud.update_idletasks()
            hud.update()

            # Assert that label text and colors are updated correctly with multimodal indicators
            cpu_text = hud.cpu_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            self.assertIn("🟢", cpu_text)
            self.assertIn("45.0%", cpu_text)
            self.assertEqual(cpu_color, "#00FFCC")

            ram_text = hud.ram_label.cget("text")
            ram_color = hud.ram_label.cget("text_color")
            self.assertIn("🟢", ram_text)
            self.assertIn("60.0%", ram_text)
            self.assertEqual(ram_color, "#00FFCC")
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_alert(self, mock_virtual_memory, mock_cpu_percent):
        # Setup high/alert values
        mock_cpu_percent.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()
        try:
            hud.update_idletasks()
            hud.update()

            # Assert high/alert emojis and colors are applied
            cpu_text = hud.cpu_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            self.assertIn("🚨", cpu_text)
            self.assertIn("85.0%", cpu_text)
            self.assertEqual(cpu_color, "#FF3333")

            ram_text = hud.ram_label.cget("text")
            ram_color = hud.ram_label.cget("text_color")
            self.assertIn("🚨", ram_text)
            self.assertIn("90.0%", ram_text)
            self.assertEqual(ram_color, "#FF3333")
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Mock the destroy method to see if pressing Escape invokes it
        with patch.object(hud, "destroy") as mock_destroy:
            # Generate Escape key event on the widget with focus
            hud.event_generate("<Escape>")
            hud.update()

            mock_destroy.assert_called_once()

        # Clean up for real
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_after_job(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()
        job_id = hud._update_job_id
        self.assertIsNotNone(job_id)

        # Spy/Mock after_cancel on the hud object to verify it cancels the job
        with patch.object(hud, "after_cancel") as mock_after_cancel:
            hud.destroy()
            mock_after_cancel.assert_called_once_with(job_id)
            self.assertIsNone(hud._update_job_id)


if __name__ == "__main__":
    unittest.main()
