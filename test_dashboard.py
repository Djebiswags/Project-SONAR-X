import unittest
from unittest.mock import patch
import dashboard


class TestDashboardHUD(unittest.TestCase):
    def test_dashboard_creation_and_telemetry(self):
        with patch("psutil.cpu_percent", return_value=15.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 40.0
            hud = dashboard.create_dashboard()

            # Check label texts and multi-modal icon
            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")
            self.assertIn("🟢 CPU Load: 15.0%", cpu_text)
            self.assertIn("RAM Usage: 40.0%", ram_text)
            self.assertIsNotNone(hud._update_job)

            # Clean up
            hud.destroy()
            self.assertIsNone(hud._update_job)

    def test_dashboard_high_cpu_indicator(self):
        with patch("psutil.cpu_percent", return_value=85.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 50.0
            hud = dashboard.create_dashboard()

            cpu_text = hud.cpu_label.cget("text")
            self.assertIn("🚨 CPU Load: 85.0%", cpu_text)

            hud.destroy()

    def test_dashboard_escape_key_closes_hud(self):
        with patch("psutil.cpu_percent", return_value=10.0), patch("psutil.virtual_memory") as mock_ram:
            mock_ram.return_value.percent = 30.0
            hud = dashboard.create_dashboard()
            hud.deiconify()
            hud.focus_force()
            hud.update()

            # Generate Escape key event
            hud.event_generate("<Escape>")
            hud.update()

            # Destroy should have been triggered
            self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
