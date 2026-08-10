import unittest
from unittest.mock import patch, MagicMock
from dashboard import create_dashboard

class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        # We can mock psutil to return predictable telemetry values
        self.cpu_patcher = patch("psutil.cpu_percent", return_value=45.0)
        self.ram_patcher = patch("psutil.virtual_memory")

        self.mock_cpu = self.cpu_patcher.start()
        self.mock_ram_obj = MagicMock()
        self.mock_ram_obj.percent = 50.0
        self.mock_ram = self.ram_patcher.start()
        self.mock_ram.return_value = self.mock_ram_obj

    def tearDown(self):
        self.cpu_patcher.stop()
        self.ram_patcher.stop()

    def test_dashboard_initial_state_under_threshold(self):
        # When CPU and RAM are under 80%, emojis should be 🟢
        hud = create_dashboard()
        try:
            # Force update to ensure the geometry and focus are handled
            hud.update()

            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")

            self.assertIn("🟢 CPU Load: 45.0%", cpu_text)
            self.assertIn("🟢 RAM Usage: 50.0%", ram_text)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#00FFCC")

            # Make sure Escape key is bound globally
            escape_bindings = hud.bind_all("<Escape>")
            self.assertTrue(escape_bindings != "")

        finally:
            hud.destroy()

    def test_dashboard_state_above_threshold(self):
        # Set CPU above 80% and RAM above 80%
        self.mock_cpu.return_value = 85.0
        self.mock_ram_obj.percent = 90.0

        hud = create_dashboard()
        try:
            hud.update()

            cpu_text = hud.cpu_label.cget("text")
            ram_text = hud.ram_label.cget("text")

            self.assertIn("🚨 CPU Load: 85.0%", cpu_text)
            self.assertIn("🚨 RAM Usage: 90.0%", ram_text)
            self.assertEqual(hud.cpu_label.cget("text_color"), "#FF3333")
        finally:
            hud.destroy()

    def test_escape_key_closes_hud(self):
        # Test that the Escape key correctly closes the HUD
        hud = create_dashboard()

        # We can mock hud.destroy to see if it gets called when Escape is pressed
        original_destroy = hud.destroy
        hud.destroy = MagicMock(side_effect=original_destroy)

        try:
            # Programmatically test keyboard events in headless CustomTkinter environment (Xvfb)
            hud.deiconify()
            hud.focus_force()
            hud.update()

            # Generate Escape key event
            hud.event_generate("<Escape>")
            hud.update()

            # Ensure destroy was called
            hud.destroy.assert_called_once()
        finally:
            # If destroy was not called or was mocked, clean up manually
            try:
                original_destroy()
            except Exception:
                pass

    def test_teardown_cancels_after_jobs(self):
        # Verify that the .after() schedule is properly cancelled on destroy
        hud = create_dashboard()
        self.assertIsNotNone(hud._update_job)

        # We mock after_cancel to ensure it gets called with the correct job ID
        hud.after_cancel = MagicMock()

        job_id = hud._update_job
        hud.destroy()

        hud.after_cancel.assert_called_once_with(job_id)
        self.assertIsNone(hud._update_job)

if __name__ == "__main__":
    unittest.main()
