import unittest
from unittest.mock import MagicMock, patch
from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    def test_escape_key_closes_hud(self):
        hud = create_dashboard()
        # Mock the destroy method of the HUD
        hud.destroy = MagicMock(side_effect=hud.destroy)

        hud.focus_force()
        hud.update()

        # Generate Escape event to simulate keyboard action
        hud.event_generate("<Escape>")
        hud.update()

        # Check that destroy was called
        hud.destroy.assert_called_once()

    def test_destroy_cancels_after_job(self):
        hud = create_dashboard()
        self.assertIsNotNone(hud._after_id)

        # Store the scheduled task ID
        after_id = hud._after_id

        # Mock after_cancel
        hud.after_cancel = MagicMock(side_effect=hud.after_cancel)

        # Call destroy and verify cleanup
        hud.destroy()

        hud.after_cancel.assert_called_with(after_id)
        self.assertIsNone(hud._after_id)

    def test_color_and_indicator_under_normal_load(self):
        hud = create_dashboard()
        with patch("psutil.cpu_percent", return_value=15.0):
            hud.update_telemetry()
            text = hud.cpu_label.cget("text")
            text_color = hud.cpu_label.cget("text_color")
            self.assertIn("🟢", text)
            self.assertIn("15.0%", text)
            self.assertEqual(text_color, "#00FFCC")

        hud.destroy()

    def test_color_and_indicator_under_high_load(self):
        hud = create_dashboard()
        with patch("psutil.cpu_percent", return_value=85.0):
            hud.update_telemetry()
            text = hud.cpu_label.cget("text")
            text_color = hud.cpu_label.cget("text_color")
            self.assertIn("🚨", text)
            self.assertIn("85.0%", text)
            self.assertEqual(text_color, "#FF3333")

        hud.destroy()


if __name__ == "__main__":
    unittest.main()
