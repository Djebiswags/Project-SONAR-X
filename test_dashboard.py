import unittest
from unittest.mock import patch
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
    def test_telemetry_normal_status(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 45.0
        mock_ram.return_value.percent = 50.0

        self.hud.update_telemetry()
        text = self.hud.cpu_label.cget("text")
        color = self.hud.cpu_label.cget("text_color")

        self.assertIn("🟢", text)
        self.assertIn("45.0%", text)
        self.assertEqual(color, "#00FFCC")

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high_load_status(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 92.5
        mock_ram.return_value.percent = 75.0

        self.hud.update_telemetry()
        text = self.hud.cpu_label.cget("text")
        color = self.hud.cpu_label.cget("text_color")

        self.assertIn("🚨", text)
        self.assertIn("92.5%", text)
        self.assertEqual(color, "#FF3333")

    def test_escape_key_closes_hud(self):
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

        destroyed = False

        def on_destroy(event):
            nonlocal destroyed
            destroyed = True

        self.hud.bind("<Destroy>", on_destroy)
        self.hud.event_generate("<Escape>")
        self.hud.update()

        self.assertTrue(destroyed)

    def test_destroy_cleans_up_resources(self):
        self.assertIsNotNone(self.hud._after_id)
        self.hud.destroy()
        self.assertIsNone(self.hud._after_id)


if __name__ == "__main__":
    unittest.main()
