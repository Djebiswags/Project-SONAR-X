import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def test_create_dashboard_and_components(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)
        self.assertTrue(hasattr(hud, "cpu_label"))
        self.assertTrue(hasattr(hud, "ram_label"))
        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_update_telemetry_normal(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 42.0
        mock_ram.return_value.percent = 55.0

        hud = dashboard.create_dashboard()
        hud.update_telemetry()

        self.assertIn("🟢 CPU Load: 42.0%", hud.cpu_label.cget("text"))
        self.assertIn("RAM Usage: 55.0%", hud.ram_label.cget("text"))
        hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_update_telemetry_high_cpu(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 92.5
        mock_ram.return_value.percent = 70.0

        hud = dashboard.create_dashboard()
        hud.update_telemetry()

        self.assertIn("🚨 CPU Load: 92.5%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        try:
            exists = bool(hud.winfo_exists())
        except Exception:
            exists = False
        self.assertFalse(exists)

    def test_destroy_cleans_up_job(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)
        hud.destroy()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
