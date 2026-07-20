import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
from dashboard import create_dashboard

class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_dashboard_initialization_and_telemetry(self, mock_virtual_memory, mock_cpu_percent):
        # Setup mocks
        mock_cpu_percent.return_value = 45.0
        mock_mem = MagicMock()
        mock_mem.percent = 60.0
        mock_virtual_memory.return_value = mock_mem

        # Instantiate dashboard (wrapped inside create_dashboard)
        hud = create_dashboard()

        # Verify the HUD is created and is of the right type
        self.assertIsInstance(hud, ctk.CTk)

        # Verify Escape key binding exists
        # In tkinter, self.bind() puts entries in the bind table, and we can check event pattern bindings
        # We can also call the escape handler manually to see if it destroys the window
        escape_bound = False
        for binding in hud.bind():
            if "Escape" in binding or hud.bind(binding):
                escape_bound = True
        self.assertTrue(escape_bound, "Escape key should be bound to window")

        # Force a telemetry update and verify labels/colors for normal state (<=80%)
        hud.update_telemetry()
        cpu_text = hud.cpu_label.cget("text")
        cpu_color = hud.cpu_label.cget("text_color")
        ram_text = hud.ram_label.cget("text")

        self.assertIn("🟢 CPU Load: 45.0%", cpu_text)
        self.assertEqual(cpu_color, "#00FFCC")
        self.assertEqual(ram_text, "RAM Usage: 60.0%")
        self.assertIsNotNone(hud._scheduled_job_id)

        # Mock high CPU (>80%) and check alert mode
        mock_cpu_percent.return_value = 92.5
        hud.update_telemetry()

        cpu_text_high = hud.cpu_label.cget("text")
        cpu_color_high = hud.cpu_label.cget("text_color")

        self.assertIn("🚨 CPU Load: 92.5%", cpu_text_high)
        self.assertEqual(cpu_color_high, "#FF3333")

        # Test destroy cancels scheduled updates
        job_id = hud._scheduled_job_id
        self.assertIsNotNone(job_id)

        # Call destroy and check cancellation (cannot easily query pending after,
        # but overriding destroy should run after_cancel and not raise any exceptions)
        hud.destroy()
        self.assertIsNone(hud._scheduled_job_id)

if __name__ == "__main__":
    unittest.main()
