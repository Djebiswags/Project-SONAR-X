import unittest
import sys
from unittest.mock import patch, MagicMock

# Mocking customtkinter and psutil so tests can run in any environment
sys.modules['customtkinter'] = MagicMock()
sys.modules['psutil'] = MagicMock()

import dashboard

class TestDashboard(unittest.TestCase):
    @patch('dashboard._import_customtkinter')
    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    def test_create_dashboard(self, mock_virtual_memory, mock_cpu_percent, mock_import_ctk):
        # Setup mock customtkinter
        mock_ctk = MagicMock()
        mock_import_ctk.return_value = mock_ctk

        # Setup mock CTk window instance
        mock_hud_instance = MagicMock()
        mock_ctk.CTk.return_value = mock_hud_instance

        # Mocking values
        mock_cpu_percent.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 45.0
        mock_virtual_memory.return_value = mock_mem

        hud = dashboard.create_dashboard()

        # Check that customtkinter was imported and CTk was instantiated
        mock_import_ctk.assert_called_once()
        mock_ctk.set_appearance_mode.assert_called_with("dark")
        mock_ctk.set_default_color_theme.assert_called_with("blue")

if __name__ == '__main__':
    unittest.main()
