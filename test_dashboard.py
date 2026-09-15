import unittest
from unittest.mock import patch, MagicMock
import dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_indicators_normal(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value = MagicMock(percent=45.0)

        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🟢", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
            self.assertIn("45.0%", hud.ram_label.cget("text"))
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_indicators_high_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 88.0
        mock_ram.return_value = MagicMock(percent=60.0)

        hud = dashboard.create_dashboard()
        hud.update_telemetry()
        try:
            self.assertIn("🚨", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_destroy_cancels_after_job(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._after_job)
        hud.destroy()
        self.assertIsNone(hud._after_job)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_escape_key_closes_hud(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroyed = []
        original_destroy = hud.destroy

        def mock_destroy():
            destroyed.append(True)
            original_destroy()

        hud.destroy = mock_destroy
        hud.event_generate("<Escape>")

        self.assertTrue(destroyed)


if __name__ == "__main__":
    unittest.main()
