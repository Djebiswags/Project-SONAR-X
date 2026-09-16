import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=45.0)
    @patch("psutil.virtual_memory")
    def test_hud_initialization_and_normal_status(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("45.0%", cpu_text)

        ram_text = hud.ram_label.cget("text")
        self.assertIn("50.0%", ram_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=85.0)
    @patch("psutil.virtual_memory")
    def test_hud_high_load_warning_icon(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 70.0
        hud = dashboard.create_dashboard()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("85.0%", cpu_text)

        hud.destroy()

    @patch("psutil.cpu_percent", return_value=10.0)
    @patch("psutil.virtual_memory")
    def test_escape_key_dismissal_and_destroy_cleanup(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        self.assertIsNotNone(hud._timer_id)

        # Generate Escape key press event
        hud.event_generate("<Escape>")
        hud.update()

        # Confirm the window destroy was triggered and timer job cleared
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
