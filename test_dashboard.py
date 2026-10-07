import unittest
from unittest.mock import patch
from dashboard import create_dashboard


class TestDashboardHUD(unittest.TestCase):
    def setUp(self):
        self.hud = create_dashboard()
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

    def tearDown(self):
        try:
            if self.hud.winfo_exists():
                self.hud.destroy()
        except Exception:
            pass

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_normal_status(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 25.0
        mock_vm.return_value.percent = 45.0

        self.hud.update_telemetry()
        self.hud.update()

        cpu_text = self.hud.cpu_label.cget("text")
        ram_text = self.hud.ram_label.cget("text")

        self.assertIn("🟢", cpu_text)
        self.assertIn("25.0%", cpu_text)
        self.assertIn("45.0%", ram_text)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_telemetry_high_cpu_status(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 92.5
        mock_vm.return_value.percent = 85.0

        self.hud.update_telemetry()
        self.hud.update()

        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("92.5%", cpu_text)

    def test_escape_key_closes_hud(self):
        self.hud.event_generate("<Key-Escape>")
        self.hud.update()
        try:
            exists = self.hud.winfo_exists()
        except Exception:
            exists = False
        self.assertFalse(exists)


if __name__ == "__main__":
    unittest.main()
