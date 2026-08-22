import unittest
from unittest.mock import MagicMock, patch

import dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_initialization_and_telemetry_normal(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value = MagicMock(percent=45.0)

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")

            self.assertIn("🟢", cpu_text)
            self.assertIn("25.0%", cpu_text)
            self.assertIn("45.0%", ram_text)
            self.assertIsNotNone(hud._after_id)
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_telemetry_high_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 92.0
        mock_ram.return_value = MagicMock(percent=75.0)

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            cpu_text = hud.cpu_label.cget("text")

            self.assertIn("🚨", cpu_text)
            self.assertIn("92.0%", cpu_text)
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_escape_key_closes_window(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        # Window should be destroyed, cancelling scheduled task
        self.assertIsNone(hud._after_id)

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_hud_destroy_cancels_after(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        hud.update()
        self.assertIsNotNone(hud._after_id)

        hud.destroy()
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
