import unittest
from unittest.mock import MagicMock, patch
import sys

# Define a clean stub for customtkinter to avoid Mock class inheritance recursion in tests
class StubCTk:
    class CTk:
        def __init__(self, *args, **kwargs):
            pass
        def title(self, *args, **kwargs):
            pass
        def geometry(self, *args, **kwargs):
            pass
        def attributes(self, *args, **kwargs):
            pass
        def grid_rowconfigure(self, *args, **kwargs):
            pass
        def grid_columnconfigure(self, *args, **kwargs):
            pass
        def bind(self, *args, **kwargs):
            pass
        def after(self, *args, **kwargs):
            pass

    class CTkLabel:
        def __init__(self, *args, **kwargs):
            pass
        def grid(self, *args, **kwargs):
            pass
        def configure(self, *args, **kwargs):
            pass

    @staticmethod
    def set_appearance_mode(mode):
        pass

    @staticmethod
    def set_default_color_theme(theme):
        pass

# Register the stub in sys.modules
sys.modules['customtkinter'] = StubCTk

import dashboard
import sonar_core

class TestSonarX(unittest.TestCase):
    def test_dashboard_import_and_initialization(self):
        # We mock set_appearance_mode and set_default_color_theme to inspect calls
        with patch.object(StubCTk, "set_appearance_mode") as mock_appearance, \
             patch.object(StubCTk, "set_default_color_theme") as mock_theme:

            # Call create_dashboard
            hud = dashboard.create_dashboard()

            # Verify appearance mode and color theme are set
            mock_appearance.assert_called_with("dark")
            mock_theme.assert_called_with("blue")

    def test_update_telemetry_low(self):
        # Test low CPU and RAM load
        with patch("psutil.cpu_percent", return_value=15.0), \
             patch("psutil.virtual_memory") as mock_vm:

            mock_vm.return_value.percent = 40.0

            hud = dashboard.create_dashboard()

            # Mock the labels' configure method
            hud.cpu_label.configure = MagicMock()
            hud.ram_label.configure = MagicMock()
            hud.after = MagicMock()

            hud.update_telemetry()

            # Verify the labels are configured with low load emojis (🟢) and colors (#00FFCC)
            hud.cpu_label.configure.assert_called_with(text="🟢 CPU Load: 15.0%", text_color="#00FFCC")
            hud.ram_label.configure.assert_called_with(text="🟢 RAM Usage: 40.0%", text_color="#00FFCC")

    def test_update_telemetry_high(self):
        # Test high CPU and RAM load
        with patch("psutil.cpu_percent", return_value=85.0), \
             patch("psutil.virtual_memory") as mock_vm:

            mock_vm.return_value.percent = 90.0

            hud = dashboard.create_dashboard()

            # Mock the labels' configure method
            hud.cpu_label.configure = MagicMock()
            hud.ram_label.configure = MagicMock()
            hud.after = MagicMock()

            hud.update_telemetry()

            # Verify the labels are configured with redline emojis (🚨) and colors (#FF3333)
            hud.cpu_label.configure.assert_called_with(text="🚨 CPU Load: 85.0%", text_color="#FF3333")
            hud.ram_label.configure.assert_called_with(text="🚨 RAM Usage: 90.0%", text_color="#FF3333")

    def test_sonar_core_load_config(self):
        # Test loading config when file does not exist
        with patch("pathlib.Path.exists", return_value=False):
            cfg = sonar_core.load_config()
            self.assertEqual(cfg, [])

if __name__ == "__main__":
    unittest.main()
