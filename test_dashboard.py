import unittest
from unittest.mock import MagicMock, patch
import sys

class MockCTk:
    def __init__(self, *args, **kwargs):
        self.title = MagicMock()
        self.geometry = MagicMock()
        self.attributes = MagicMock()
        self.bind = MagicMock()
        self.grid_rowconfigure = MagicMock()
        self.grid_columnconfigure = MagicMock()
        self.after = MagicMock()

# We will patch 'dashboard._import_customtkinter' to return our Mock ctk.
import dashboard

class TestSonarDashboard(unittest.TestCase):
    @patch("dashboard._import_customtkinter")
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_create_dashboard_initialization(self, mock_virtual_memory, mock_cpu_percent, mock_import_ctk):
        # Setup ctk mock
        mock_ctk = MagicMock()
        mock_ctk.CTk = MockCTk

        # Make CTkLabel return a new MagicMock for each label instance
        mock_ctk.CTkLabel.side_effect = lambda *args, **kwargs: MagicMock()
        mock_import_ctk.return_value = mock_ctk

        # Mock psutil values for normal telemetry
        mock_cpu_percent.return_value = 45.2
        mock_mem = MagicMock()
        mock_mem.percent = 60.5
        mock_virtual_memory.return_value = mock_mem

        # Call create_dashboard
        hud = dashboard.create_dashboard()

        # Check ctk methods called
        mock_ctk.set_appearance_mode.assert_called_with("dark")
        mock_ctk.set_default_color_theme.assert_called_with("blue")

        # Verify window configurations
        hud.title.assert_called_with("SONAR-X | Live Telemetry")
        hud.geometry.assert_called_with("350x220")
        hud.attributes.assert_called_with("-topmost", True)

        # Check that Escape is bound
        hud.bind.assert_any_call("<Escape>", unittest.mock.ANY)

        # Check row and column layout configuration
        hud.grid_rowconfigure.assert_any_call(0, weight=1)
        hud.grid_rowconfigure.assert_any_call(1, weight=1)
        hud.grid_rowconfigure.assert_any_call(2, weight=1)
        hud.grid_columnconfigure.assert_any_call(0, weight=1)

        # Verify that labels are created with expected params
        mock_ctk.CTkLabel.assert_any_call(
            hud,
            text="Press ESC to exit",
            font=("Helvetica", 11, "italic"),
            text_color="#777777"
        )

        # Verify update_telemetry was called and configure was executed with normal state colors/emojis
        hud.cpu_label.configure.assert_called_with(text="🟢 CPU Load: 45.2%", text_color="#00FFCC")
        hud.ram_label.configure.assert_called_with(text="🟢 RAM Usage: 60.5%", text_color="#DCE4EE")

    @patch("dashboard._import_customtkinter")
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_update_telemetry_high_usage(self, mock_virtual_memory, mock_cpu_percent, mock_import_ctk):
        # Setup ctk mock
        mock_ctk = MagicMock()
        mock_ctk.CTk = MockCTk
        mock_ctk.CTkLabel.side_effect = lambda *args, **kwargs: MagicMock()
        mock_import_ctk.return_value = mock_ctk

        # Mock psutil values for high telemetry (>80%)
        mock_cpu_percent.return_value = 88.5
        mock_mem = MagicMock()
        mock_mem.percent = 92.1
        mock_virtual_memory.return_value = mock_mem

        # Call create_dashboard
        hud = dashboard.create_dashboard()

        # Verify labels reflect critical warning state with 🚨 emoji and red text (#FF3333)
        hud.cpu_label.configure.assert_called_with(text="🚨 CPU Load: 88.5%", text_color="#FF3333")
        hud.ram_label.configure.assert_called_with(text="🚨 RAM Usage: 92.1%", text_color="#FF3333")

if __name__ == "__main__":
    unittest.main()
