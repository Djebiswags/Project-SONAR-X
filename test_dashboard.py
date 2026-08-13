import unittest
from unittest.mock import patch, MagicMock
import dashboard

class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_normal(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 45.0
        mock_ram = MagicMock()
        mock_ram.percent = 50.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        hud.update_idletasks()
        hud.update()

        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 45.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "🟢 RAM Usage: 50.0%")
        self.assertIsNotNone(hud._after_id)

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_high(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 85.0
        mock_ram = MagicMock()
        mock_ram.percent = 90.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        hud.update_idletasks()
        hud.update()

        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 85.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertEqual(hud.ram_label.cget("text"), "🚨 RAM Usage: 90.0%")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        destroyed = False
        original_destroy = hud.destroy
        def mock_destroy():
            nonlocal destroyed
            destroyed = True
            original_destroy()

        hud.destroy = mock_destroy
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroyed)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_after(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        hud.update_idletasks()
        hud.update()

        after_id = hud._after_id
        self.assertIsNotNone(after_id)

        cancelled_id = None
        original_after_cancel = hud.after_cancel
        def mock_after_cancel(id_):
            nonlocal cancelled_id
            cancelled_id = id_
            original_after_cancel(id_)

        hud.after_cancel = mock_after_cancel
        hud.destroy()

        self.assertEqual(cancelled_id, after_id)

if __name__ == "__main__":
    unittest.main()
