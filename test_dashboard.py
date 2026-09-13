import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def test_hud_initialization_and_telemetry(self):
        with patch("psutil.cpu_percent", return_value=45.0), \
             patch("psutil.virtual_memory") as mock_mem:
            mock_mem.return_value.percent = 50.0
            hud = dashboard.create_dashboard()
            self.assertIn("🟢 CPU Load: 45.0%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 50.0%")
            hud.destroy()

    def test_high_cpu_multi_modal_indicator(self):
        with patch("psutil.cpu_percent", return_value=95.0), \
             patch("psutil.virtual_memory") as mock_mem:
            mock_mem.return_value.percent = 60.0
            hud = dashboard.create_dashboard()
            self.assertIn("🚨 CPU Load: 95.0%", hud.cpu_label.cget("text"))
            hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")
        hud.update()
        # After Escape is pressed, destroy() is invoked so window is destroyed.
        with self.assertRaises(Exception):
            hud.winfo_exists()


if __name__ == "__main__":
    unittest.main()
