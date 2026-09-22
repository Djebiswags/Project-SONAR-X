import unittest
from unittest.mock import patch, MagicMock
import dashboard


class TestDashboardHUD(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_hud_initialization_and_indicators(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_vm.return_value = MagicMock(percent=45.0)

        hud = dashboard.create_dashboard()
        hud.update()

        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("25.0%", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))

        mock_cpu.return_value = 88.0
        hud.update_telemetry()
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("88.0%", hud.cpu_label.cget("text"))

        hud.destroy()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_vm.return_value = MagicMock(percent=20.0)

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
