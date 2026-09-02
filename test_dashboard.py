import _tkinter
import unittest
from unittest.mock import MagicMock, patch

import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_normal_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 25.0
        mock_ram.return_value = MagicMock(percent=40.0)

        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🟢", hud.cpu_label.cget("text"))
            self.assertIn("25.0%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
            self.assertEqual(hud.ram_label.cget("text"), "RAM Usage: 40.0%")
        finally:
            hud.destroy()

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_telemetry_high_load(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 92.5
        mock_ram.return_value = MagicMock(percent=75.0)

        hud = dashboard.create_dashboard()
        try:
            self.assertIn("🚨", hud.cpu_label.cget("text"))
            self.assertIn("92.5%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        hud.update()

        with self.assertRaises(_tkinter.TclError):
            # Once destroyed, cget or state access will raise TclError
            hud.cget("title")

    @patch("psutil.virtual_memory")
    @patch("psutil.cpu_percent")
    def test_destroy_cancels_timer(self, mock_cpu, mock_ram):
        mock_cpu.return_value = 10.0
        mock_ram.return_value = MagicMock(percent=20.0)

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._timer)

        with patch.object(hud, "after_cancel") as mock_cancel:
            timer_id = hud._timer
            hud.destroy()
            mock_cancel.assert_called_once_with(timer_id)
            self.assertIsNone(hud._timer)


if __name__ == "__main__":
    unittest.main()
