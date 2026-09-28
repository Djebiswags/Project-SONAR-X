import unittest
from unittest.mock import MagicMock, patch
import dashboard


class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        self.hud = dashboard.create_dashboard()

    def tearDown(self):
        try:
            self.hud.destroy()
        except Exception:
            pass

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_normal(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram_obj = MagicMock()
        mock_ram_obj.percent = 40.0
        mock_ram.return_value = mock_ram_obj

        self.hud.update_telemetry()

        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("25.0%", cpu_text)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 85.0
        mock_ram_obj = MagicMock()
        mock_ram_obj.percent = 70.0
        mock_ram.return_value = mock_ram_obj

        self.hud.update_telemetry()

        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("85.0%", cpu_text)

    def test_escape_key_closes_hud(self):
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

        with patch.object(self.hud, "destroy", wraps=self.hud.destroy) as mock_destroy:
            self.hud.event_generate("<Escape>")
            self.hud.update()
            mock_destroy.assert_called_once()

    def test_destroy_cleanup(self):
        self.assertIsNotNone(self.hud._update_job)
        self.hud.destroy()
        self.assertIsNone(self.hud._update_job)


if __name__ == "__main__":
    unittest.main()
