import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.hud = dashboard.create_dashboard()

    def tearDown(self):
        try:
            if self.hud.winfo_exists():
                self.hud.destroy()
        except Exception:
            pass

    def test_dashboard_initialization(self):
        self.assertIsNotNone(self.hud)
        self.assertIsNotNone(self.hud._after_id)
        self.assertIn("CPU Load:", self.hud.cpu_label.cget("text"))
        self.assertIn("RAM Usage:", self.hud.ram_label.cget("text"))

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_update_telemetry_low_cpu(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_ram.return_value.percent = 40.0

        self.hud.update_telemetry()
        label_text = self.hud.cpu_label.cget("text")
        text_color = self.hud.cpu_label.cget("text_color")

        self.assertIn("🟢 CPU Load: 15.0%", label_text)
        self.assertEqual(text_color, "#00FFCC")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_update_telemetry_high_cpu(self, mock_ram, mock_cpu):
        mock_cpu.return_value = 92.5
        mock_ram.return_value.percent = 70.0

        self.hud.update_telemetry()
        label_text = self.hud.cpu_label.cget("text")
        text_color = self.hud.cpu_label.cget("text_color")

        self.assertIn("🚨 CPU Load: 92.5%", label_text)
        self.assertEqual(text_color, "#FF3333")

    def test_escape_key_dismisses_window(self):
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()
        self.hud.event_generate("<Escape>")
        self.hud.update()
        try:
            exists = self.hud.winfo_exists()
        except Exception:
            exists = 0
        self.assertEqual(exists, 0)

    def test_destroy_cancels_after_job(self):
        after_id = self.hud._after_id
        self.assertIsNotNone(after_id)
        self.hud.destroy()
        self.assertIsNone(self.hud._after_id)


if __name__ == "__main__":
    unittest.main()
