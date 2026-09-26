import unittest
from unittest.mock import patch
from dashboard import create_dashboard


class TestDashboard(unittest.TestCase):
    def test_dashboard_creation_and_telemetry(self):
        with patch("psutil.cpu_percent", return_value=45.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 50.0
            hud = create_dashboard()
            hud.update()

            self.assertIn("🟢 CPU Load: 45.0%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 50.0%")
            hud.destroy()

    def test_dashboard_high_cpu_indicator(self):
        with patch("psutil.cpu_percent", return_value=88.5), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 60.0
            hud = create_dashboard()
            hud.update()

            self.assertIn("🚨 CPU Load: 88.5%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
            hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Simulate Escape key press
        hud.event_generate("<Escape>")
        hud.update()

        # After Escape is pressed, destroy() should be executed
        self.assertIsNone(hud._after_job)

    def test_destroy_cleans_up_resources(self):
        hud = create_dashboard()
        hud.update()
        self.assertIsNotNone(hud._after_job)

        hud.destroy()
        self.assertIsNone(hud._after_job)


if __name__ == "__main__":
    unittest.main()
