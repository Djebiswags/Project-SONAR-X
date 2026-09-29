import unittest
from unittest.mock import patch

import dashboard


class TestSonarHUD(unittest.TestCase):
    def test_dashboard_creation_and_telemetry_formatting(self):
        with patch("psutil.cpu_percent", return_value=15.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 42.0
            hud = dashboard.create_dashboard()
            try:
                cpu_text = hud.cpu_label.cget("text")
                ram_text = hud.ram_label.cget("text")

                self.assertIn("🟢", cpu_text)
                self.assertIn("15.0%", cpu_text)
                self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
                self.assertEqual(ram_text, "RAM Usage: 42.0%")
            finally:
                hud.destroy()

    def test_high_cpu_load_warning_indicator(self):
        with patch("psutil.cpu_percent", return_value=88.5), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 50.0
            hud = dashboard.create_dashboard()
            try:
                cpu_text = hud.cpu_label.cget("text")

                self.assertIn("🚨", cpu_text)
                self.assertIn("88.5%", cpu_text)
                self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
            finally:
                hud.destroy()

    def test_keyboard_escape_dismisses_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Generate Escape keypress event
        hud.event_generate("<Escape>")
        hud.update()

        # Check if destroy was triggered and update job cleared
        self.assertIsNone(hud._update_job)

    def test_clean_destroy_cancels_update_job(self):
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._update_job)
        hud.destroy()
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
