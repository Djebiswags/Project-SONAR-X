import unittest
from unittest.mock import patch
import dashboard


class TestSonarDashboard(unittest.TestCase):
    def test_dashboard_initialization_and_telemetry(self):
        with patch("psutil.cpu_percent", return_value=15.0), \
             patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 45.0
            hud = dashboard.create_dashboard()
            try:
                cpu_text = hud.cpu_label.cget("text")
                self.assertIn("🟢", cpu_text)
                self.assertIn("15.0%", cpu_text)

                ram_text = hud.ram_label.cget("text")
                self.assertIn("45.0%", ram_text)
            finally:
                hud.destroy()

    def test_high_cpu_telemetry_icon_and_color(self):
        with patch("psutil.cpu_percent", return_value=88.5), \
             patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 50.0
            hud = dashboard.create_dashboard()
            try:
                cpu_text = hud.cpu_label.cget("text")
                self.assertIn("🚨", cpu_text)
                self.assertIn("88.5%", cpu_text)
                self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
            finally:
                hud.destroy()

    def test_escape_key_closes_hud(self):
        with patch("psutil.cpu_percent", return_value=10.0), \
             patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 30.0
            hud = dashboard.create_dashboard()
            hud.deiconify()
            hud.focus_force()
            hud.update()

            hud.event_generate("<Escape>")
            hud.update()

            # The window should be destroyed or destroyed on Tcl level
            with self.assertRaises(Exception):
                hud.winfo_exists()

    def test_destroy_cleanup(self):
        with patch("psutil.cpu_percent", return_value=20.0), \
             patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 40.0
            hud = dashboard.create_dashboard()
            self.assertIsNotNone(hud._after_id)
            hud.destroy()
            self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
