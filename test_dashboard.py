import unittest
from unittest.mock import patch
import dashboard


class TestDashboard(unittest.TestCase):
    @patch("psutil.cpu_percent", return_value=15.0)
    @patch("psutil.virtual_memory")
    def test_hud_normal_telemetry(self, mock_ram, mock_cpu):
        mock_ram.return_value.percent = 40.0
        hud = dashboard.create_dashboard()
        self.addCleanup(lambda: self._safe_destroy(hud))

        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("40.0%", hud.ram_label.cget("text"))

    @patch("psutil.cpu_percent", return_value=85.0)
    @patch("psutil.virtual_memory")
    def test_hud_high_cpu_telemetry(self, mock_ram, mock_cpu):
        mock_ram.return_value.percent = 50.0
        hud = dashboard.create_dashboard()
        self.addCleanup(lambda: self._safe_destroy(hud))

        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("85.0%", hud.cpu_label.cget("text"))

    def _safe_destroy(self, hud):
        try:
            if hud.winfo_exists():
                hud.destroy()
        except Exception:
            pass

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_hud_escape_key_closes(self, mock_ram, mock_cpu):
        mock_ram.return_value.percent = 30.0
        hud = dashboard.create_dashboard()
        self.addCleanup(lambda: self._safe_destroy(hud))

        hud.deiconify()
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")
        hud.update()

        destroyed = False
        try:
            destroyed = not hud.winfo_exists()
        except Exception:
            destroyed = True
        self.assertTrue(destroyed)

    @patch("psutil.cpu_percent", return_value=20.0)
    @patch("psutil.virtual_memory")
    def test_hud_destroy_cleans_timer(self, mock_ram, mock_cpu):
        mock_ram.return_value.percent = 30.0
        hud = dashboard.create_dashboard()

        timer_id = hud._timer_id
        self.assertIsNotNone(timer_id)
        hud.destroy()
        self.assertIsNone(hud._timer_id)


if __name__ == "__main__":
    unittest.main()
