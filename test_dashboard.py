import unittest
from unittest.mock import patch, MagicMock
from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_creation_and_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 15.0

        mock_ram = MagicMock()
        mock_ram.percent = 45.0
        mock_virtual_memory.return_value = mock_ram

        hud = create_dashboard()

        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Check initial/updated text and color
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

        self.assertIn("📊", hud.ram_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_redline_indicator(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 92.0

        mock_ram = MagicMock()
        mock_ram.percent = 85.0
        mock_virtual_memory.return_value = mock_ram

        hud = create_dashboard()

        # Check updated text and color under redline condition (>80%)
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("92.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_bind(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = create_dashboard()

        # Verify that pressing Escape triggers window destruction
        destroyed = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroyed
            destroyed = True
            original_destroy()

        hud.destroy = mock_destroy
        hud.focus_force()
        hud.update()
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroyed)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_after_cancel_on_destroy(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = create_dashboard()
        after_id = hud._after_id
        self.assertIsNotNone(after_id)

        cancel_called_with = None
        original_cancel = hud.after_cancel

        def mock_cancel(aid):
            nonlocal cancel_called_with
            cancel_called_with = aid
            original_cancel(aid)

        hud.after_cancel = mock_cancel
        hud.destroy()

        self.assertEqual(cancel_called_with, after_id)


if __name__ == "__main__":
    unittest.main()
