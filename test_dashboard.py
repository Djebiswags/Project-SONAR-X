import unittest
from unittest.mock import patch, MagicMock
from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We need to initialize customtkinter or let it be mocked if preferred,
        # but since we are running under xvfb-run, we can instantiate the actual UI!
        pass

    def setUp(self):
        # Patch psutil to control return values
        self.cpu_patch = patch("psutil.cpu_percent", return_value=45.0)
        self.ram_patch = patch("psutil.virtual_memory")

        self.mock_cpu = self.cpu_patch.start()
        self.mock_ram = self.ram_patch.start()

        mock_virtual_mem = MagicMock()
        mock_virtual_mem.percent = 50.0
        self.mock_ram.return_value = mock_virtual_mem

    def tearDown(self):
        self.cpu_patch.stop()
        self.ram_patch.stop()

    def test_dashboard_initialization_and_indicator(self):
        # Create dashboard under test
        hud = create_dashboard()

        # CPU is 45.0%, indicator should be green circle (🟢)
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("45.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

        # Now mock CPU load above 80% and call update_telemetry manually to check red light (🚨)
        self.mock_cpu.return_value = 85.0
        hud.update_telemetry()

        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("85.0%", hud.cpu_label.cget("text"))
        self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")

        # Clean up
        hud.destroy()

    def test_escape_key_closes_hud(self):
        hud = create_dashboard()

        # Bring HUD to focus for headless event testing
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Track if destroy was called
        destroy_called = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroy_called
            destroy_called = True
            original_destroy()

        hud.destroy = mock_destroy

        # Generate global Escape key press event
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroy_called)


if __name__ == "__main__":
    unittest.main()
