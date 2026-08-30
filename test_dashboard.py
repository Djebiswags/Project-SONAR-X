import unittest
from unittest.mock import patch
import dashboard


class TestDashboardUX(unittest.TestCase):
    def setUp(self):
        self.hud = dashboard.create_dashboard()
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

    def tearDown(self):
        try:
            self.hud.destroy()
        except Exception:
            pass

    @patch("psutil.cpu_percent", return_value=45.0)
    @patch("psutil.virtual_memory")
    def test_normal_telemetry_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        self.hud.update_telemetry()
        self.assertIn("🟢", self.hud.cpu_label.cget("text"))
        self.assertIn("45.0%", self.hud.cpu_label.cget("text"))

    @patch("psutil.cpu_percent", return_value=95.0)
    @patch("psutil.virtual_memory")
    def test_high_load_telemetry_indicator(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 30.0
        self.hud.update_telemetry()
        self.assertIn("🚨", self.hud.cpu_label.cget("text"))
        self.assertIn("95.0%", self.hud.cpu_label.cget("text"))

    def test_escape_key_closes_window(self):
        self.hud.event_generate("<Escape>")
        self.hud.update()
        with self.assertRaises(Exception):
            self.hud.winfo_exists()

    def test_destroy_cleans_up_after_job(self):
        self.assertIsNotNone(self.hud._update_job)
        self.hud.destroy()
        self.assertIsNone(self.hud._update_job)


if __name__ == "__main__":
    unittest.main()
