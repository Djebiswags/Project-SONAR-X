import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_normal_cpu(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_vm.return_value.percent = 40.0

        hud = dashboard.create_dashboard()
        self.assertIn("⚡ CPU Load: 25.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertIn("RAM Usage: 40.0%", hud.ram_label.cget("text"))
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_high_cpu_indicator(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 85.0
        mock_vm.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        self.assertIn("🚨 CPU Load: 85.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_escape_key_dismissal(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_vm.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Simulate Escape key press
        hud.event_generate("<Escape>")
        hud.update()

        # Verify window is destroyed / invalid Tcl handle
        with self.assertRaises(Exception):
            hud.winfo_exists()


if __name__ == "__main__":
    unittest.main()
