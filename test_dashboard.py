import unittest
from unittest.mock import MagicMock, patch

import dashboard


class TestSonarDashboard(unittest.TestCase):
    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_dashboard_creation_and_multimodal_indicators(
        self, mock_virtual_memory, mock_cpu_percent
    ):
        # Mock high resource usage
        mock_cpu_percent.return_value = 85.0
        mock_ram = MagicMock()
        mock_ram.percent = 90.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        hud.update()

        # Check if the text contains high-load emojis (🚨)
        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")
        self.assertIn("🚨", cpu_text)
        self.assertIn("🚨", ram_text)

        # Mock normal resource usage
        mock_cpu_percent.return_value = 12.0
        mock_ram.percent = 40.0

        hud.update_telemetry()
        hud.update()

        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")
        self.assertIn("🟢", cpu_text)
        self.assertIn("🟢", ram_text)

        hud.destroy()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_escape_key_closes_window(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()

        # Follow critical learning for headless keyboard event testing
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Use patch to check if destroy was called
        with patch.object(hud, "destroy", wraps=hud.destroy) as mock_destroy:
            hud.event_generate("<Escape>")
            hud.update()
            mock_destroy.assert_called_once()

    @patch("dashboard.psutil.cpu_percent")
    @patch("dashboard.psutil.virtual_memory")
    def test_after_cleanup_on_destroy(self, mock_virtual_memory, mock_cpu_percent):
        mock_cpu_percent.return_value = 10.0
        mock_ram = MagicMock()
        mock_ram.percent = 10.0
        mock_virtual_memory.return_value = mock_ram

        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._after_id)

        # Destroy the hud, which should cancel the after callback and clear self._after_id
        hud.destroy()
        self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
