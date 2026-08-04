import unittest
from unittest.mock import patch

from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_update_telemetry_low_cpu(self, mock_virtual_mem, mock_cpu_percent):
        mock_cpu_percent.return_value = 45.0
        mock_virtual_mem.return_value.percent = 50.0

        hud = create_dashboard()

        hud.update_telemetry()

        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("50.0%", hud.ram_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_update_telemetry_high_cpu(self, mock_virtual_mem, mock_cpu_percent):
        mock_cpu_percent.return_value = 85.0
        mock_virtual_mem.return_value.percent = 70.0

        hud = create_dashboard()
        hud.update_telemetry()

        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("85.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_destroys(self, mock_virtual_mem, mock_cpu_percent):
        mock_cpu_percent.return_value = 20.0
        mock_virtual_mem.return_value.percent = 30.0

        hud = create_dashboard()

        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroy_called = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroy_called
            destroy_called = True
            original_destroy()

        hud.destroy = mock_destroy
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroy_called)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_destroy_cancels_after(self, mock_virtual_mem, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_virtual_mem.return_value.percent = 20.0

        hud = create_dashboard()

        self.assertIsNotNone(hud._update_job_id)

        hud.destroy()
        self.assertIsNone(hud._update_job_id)


if __name__ == "__main__":
    unittest.main()
