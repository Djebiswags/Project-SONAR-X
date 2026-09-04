import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.hud = dashboard.create_dashboard()
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

    def tearDown(self):
        try:
            self.hud.destroy()
        except Exception:
            pass

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_normal_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 42.0
        mock_ram.return_value.percent = 35.0

        self.hud.update_telemetry()
        self.hud.update()

        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("42.0%", cpu_text)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 88.5
        mock_ram.return_value.percent = 50.0

        self.hud.update_telemetry()
        self.hud.update()

        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("88.5%", cpu_text)

    def test_escape_key_dismisses_hud(self):
        destroyed = False

        def on_destroy():
            nonlocal destroyed
            destroyed = True

        self.hud.bind("<Destroy>", lambda e: on_destroy())
        self.hud.event_generate("<Escape>")
        self.hud.update()

        self.assertTrue(destroyed)

    def test_destroy_cancels_timer(self):
        self.assertIsNotNone(self.hud._timer)
        self.hud.destroy()
        self.assertIsNone(self.hud._timer)


if __name__ == "__main__":
    unittest.main()
