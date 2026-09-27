import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_nominal(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_vm.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            self.assertIn("🟢 25.0%", hud.cpu_label.cget("text"))
            self.assertIn("45.0%", hud.ram_label.cget("text"))
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_high_load(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 85.5
        mock_vm.return_value.percent = 70.0

        hud = dashboard.create_dashboard()
        try:
            hud.update()
            self.assertIn("🚨 85.5%", hud.cpu_label.cget("text"))
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_vm.return_value.percent = 20.0

        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        hud.event_generate("<Escape>")
        try:
            hud.update()
            exists = bool(hud.winfo_exists())
        except Exception:
            exists = False

        self.assertFalse(exists)


if __name__ == "__main__":
    unittest.main()
