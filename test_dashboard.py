import unittest
from unittest.mock import MagicMock, patch
import dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("dashboard.psutil")
    @patch("customtkinter.CTk.after")
    @patch("customtkinter.CTk.after_cancel")
    @patch("customtkinter.CTk.bind")
    def test_hud_initialization_and_telemetry(self, mock_bind, mock_after_cancel, mock_after, mock_psutil):
        # Setup psutil mock values
        mock_psutil.cpu_percent.return_value = 45.0
        mock_virtual_memory = MagicMock()
        mock_virtual_memory.percent = 55.0
        mock_psutil.virtual_memory.return_value = mock_virtual_memory

        # Instantiating create_dashboard (which creates SonarHUD)
        hud = dashboard.create_dashboard()

        # Check that we bind Escape
        mock_bind.assert_any_call("<Escape>", unittest.mock.ANY)

        # Check telemetry label values
        self.assertEqual(hud.cpu_label.cget("text"), "🟢 CPU Load: 45.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")
        self.assertEqual(hud.ram_label.cget("text"), "🟢 RAM Usage: 55.0%")
        self.assertEqual(hud.ram_label.cget("text_color"), "#00FFCC")

        # Check teardown cancels timer
        hud.destroy()
        mock_after_cancel.assert_called_once()

    @patch("dashboard.psutil")
    @patch("customtkinter.CTk.after")
    @patch("customtkinter.CTk.after_cancel")
    @patch("customtkinter.CTk.bind")
    def test_hud_high_telemetry_indicators(self, mock_bind, mock_after_cancel, mock_after, mock_psutil):
        # Setup psutil mock values for high load
        mock_psutil.cpu_percent.return_value = 85.0
        mock_virtual_memory = MagicMock()
        mock_virtual_memory.percent = 90.0
        mock_psutil.virtual_memory.return_value = mock_virtual_memory

        hud = dashboard.create_dashboard()

        # Check red/alert emoji and color
        self.assertEqual(hud.cpu_label.cget("text"), "🚨 CPU Load: 85.0%")
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        self.assertEqual(hud.ram_label.cget("text"), "🚨 RAM Usage: 90.0%")
        self.assertEqual(hud.ram_label.cget("text_color"), "#FF3333")

        hud.destroy()


if __name__ == "__main__":
    unittest.main()
