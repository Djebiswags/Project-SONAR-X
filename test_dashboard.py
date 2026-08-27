import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_creation_and_telemetry(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_vm.return_value.percent = 45.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("25", hud.cpu_label.cget("text"))
        self.assertIn("45", hud.ram_label.cget("text"))
        self.assertIsNotNone(hud._update_job)

        hud.destroy()
        self.assertIsNone(hud._update_job)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_high_cpu_indicator(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 92.0
        mock_vm.return_value.percent = 50.0

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

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

        # Generate Escape key event
        hud.event_generate("<Escape>")
        hud.update()

        # The window should be destroyed (or self._update_job reset to None)
        self.assertIsNone(hud._update_job)


if __name__ == "__main__":
    unittest.main()
