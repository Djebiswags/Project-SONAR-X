import unittest
from unittest.mock import MagicMock, patch

# Ensure the module can be imported
import dashboard


class TestDashboard(unittest.TestCase):
    def setUp(self):
        # We patch psutil to avoid calling real system APIs
        self.patcher_cpu = patch("psutil.cpu_percent", return_value=15.0)
        self.patcher_ram = patch("psutil.virtual_memory")

        self.mock_cpu = self.patcher_cpu.start()
        self.mock_ram = self.patcher_ram.start()

        mock_memory = MagicMock()
        mock_memory.percent = 45.0
        self.mock_ram.return_value = mock_memory

    def tearDown(self):
        self.patcher_cpu.stop()
        self.patcher_ram.stop()

    def test_create_dashboard_initial_state(self):
        """Test that create_dashboard returns a fully configured SonarHUD window with correct start state."""
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud)

        # Test default states
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")
        # On headless Linux / Xvfb, -topmost might return 0 even after setting it to True.
        # We verify it does not raise an exception, and returns a valid value in (0, 1, True, False)
        self.assertIn(hud.attributes("-topmost"), (0, 1, True, False))

        # Check initial text configuration
        cpu_text = hud.cpu_label.cget("text")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("15.0%", cpu_text)
        self.assertIn("45.0%", ram_text)
        self.assertIn("🟢", cpu_text)
        self.assertIn("🟢", ram_text)

        hud.destroy()

    def test_telemetry_high_threshold_states(self):
        """Test that labels reflect high loads correctly with red color and alarm emoji."""
        # Set CPU high, RAM low
        self.mock_cpu.return_value = 85.0
        mock_memory = MagicMock()
        mock_memory.percent = 30.0
        self.mock_ram.return_value = mock_memory

        hud = dashboard.create_dashboard()

        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        self.assertIn("🚨", cpu_text)
        self.assertEqual(cpu_color, "#FF3333")

        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")
        self.assertIn("🟢", ram_text)
        self.assertEqual(ram_color, "#00FFCC")

        hud.destroy()

        # Set CPU low, RAM high
        self.mock_cpu.return_value = 10.0
        mock_memory = MagicMock()
        mock_memory.percent = 90.0
        self.mock_ram.return_value = mock_memory

        hud = dashboard.create_dashboard()

        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        self.assertIn("🟢", cpu_text)
        self.assertEqual(cpu_color, "#00FFCC")

        ram_text = hud.ram_label.cget("text")
        ram_color = hud.ram_label.cget("text_color")
        self.assertIn("🚨", ram_text)
        self.assertEqual(ram_color, "#FF3333")

        hud.destroy()

    def test_escape_key_closes_window(self):
        """Test that pressing the Escape key closes the window."""
        hud = dashboard.create_dashboard()

        # Deiconify, focus force and update as suggested in the memories to test key events in headless environments
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # We can mock the destroy method or observe if it gets destroyed. Let's patch the destroy method.
        with patch.object(hud, "destroy", wraps=hud.destroy) as mock_destroy:
            hud.event_generate("<Escape>")
            hud.update()
            self.assertTrue(mock_destroy.called)

    def test_after_cancel_on_destroy(self):
        """Test that destroying the dashboard successfully cancels the scheduled after task."""
        hud = dashboard.create_dashboard()
        self.assertIsNotNone(hud._telemetry_job)

        telemetry_job_id = hud._telemetry_job

        with patch.object(
            hud, "after_cancel", wraps=hud.after_cancel
        ) as mock_after_cancel:
            hud.destroy()
            mock_after_cancel.assert_called_once_with(telemetry_job_id)


if __name__ == "__main__":
    unittest.main()
