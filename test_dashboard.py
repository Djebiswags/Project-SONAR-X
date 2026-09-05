import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    def setUp(self):
        try:
            self.hud = dashboard.create_dashboard()
            self.hud.deiconify()
            self.hud.focus_force()
            self.hud.update()
        except Exception as e:
            self.skipTest(f"GUI environment not available: {e}")

    def tearDown(self):
        if hasattr(self, "hud"):
            try:
                if self.hud.winfo_exists():
                    self.hud.destroy()
            except Exception:
                pass

    def is_alive(self, widget):
        try:
            return bool(widget.winfo_exists())
        except Exception:
            return False

    @patch("psutil.cpu_percent", return_value=25.0)
    @patch("psutil.virtual_memory")
    def test_update_telemetry_normal(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 40.0
        self.hud.update_telemetry()
        cpu_text = self.hud.cpu_label.cget("text")
        ram_text = self.hud.ram_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("25.0%", cpu_text)
        self.assertIn("40.0%", ram_text)

    @patch("psutil.cpu_percent", return_value=85.0)
    @patch("psutil.virtual_memory")
    def test_update_telemetry_high_cpu(self, mock_vm, mock_cpu):
        mock_vm.return_value.percent = 70.0
        self.hud.update_telemetry()
        cpu_text = self.hud.cpu_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("85.0%", cpu_text)

    def test_escape_key_closes_hud(self):
        self.hud.update()
        self.hud.event_generate("<Escape>")
        self.hud.update()
        self.assertFalse(self.is_alive(self.hud))

    def test_destroy_cancels_after_job(self):
        self.assertIsNotNone(self.hud._after_id)
        self.hud.destroy()
        self.assertIsNone(self.hud._after_id)
        self.assertFalse(self.is_alive(self.hud))


if __name__ == "__main__":
    unittest.main()
