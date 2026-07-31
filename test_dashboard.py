import unittest
from unittest.mock import patch, MagicMock
import customtkinter as ctk
import dashboard


class TestSonarHUD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Prevent actually showing gui windows during tests
        ctk.set_appearance_mode("dark")

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_initial_telemetry_low(self, mock_virtual_mem, mock_cpu):
        # Setup mock low usage values (e.g. 10% CPU and 30% RAM)
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 30.0
        mock_virtual_mem.return_value = mock_mem

        # Create instance of hud and prevent self.after from scheduling a real loop
        with patch.object(ctk.CTk, "after", return_value="after_id_123"):
            hud = dashboard.create_dashboard()
            self.assertIsNotNone(hud)

            # Check that low usage has 🟢 emoji and correct colors
            cpu_text = hud.cpu_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            ram_text = hud.ram_label.cget("text")
            ram_color = hud.ram_label.cget("text_color")

            self.assertIn("🟢", cpu_text)
            self.assertIn("10.0%", cpu_text)
            self.assertEqual(cpu_color, "#00FFCC")

            self.assertIn("🟢", ram_text)
            self.assertIn("30.0%", ram_text)
            self.assertEqual(ram_color, "#FFFFFF")

            # Clean up window
            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_telemetry_high_threshold(self, mock_virtual_mem, mock_cpu):
        # Setup mock high usage values (e.g. 85% CPU and 90% RAM)
        mock_cpu.return_value = 85.0
        mock_mem = MagicMock()
        mock_mem.percent = 90.0
        mock_virtual_mem.return_value = mock_mem

        with patch.object(ctk.CTk, "after", return_value="after_id_456"):
            hud = dashboard.create_dashboard()

            # Check that high usage has 🚨 emoji and red colors
            cpu_text = hud.cpu_label.cget("text")
            cpu_color = hud.cpu_label.cget("text_color")
            ram_text = hud.ram_label.cget("text")
            ram_color = hud.ram_label.cget("text_color")

            self.assertIn("🚨", cpu_text)
            self.assertIn("85.0%", cpu_text)
            self.assertEqual(cpu_color, "#FF3333")

            self.assertIn("🚨", ram_text)
            self.assertIn("90.0%", ram_text)
            self.assertEqual(ram_color, "#FF3333")

            hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_destroys_hud(self, mock_virtual_mem, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_mem.return_value = mock_mem

        with patch.object(ctk.CTk, "after", return_value="after_id_escape"):
            hud = dashboard.create_dashboard()

            # Use deiconify, focus_force, and update to prepare headless keyboard test
            hud.deiconify()
            hud.focus_force()
            hud.update()

            # Mock self.destroy method to verify it gets called
            hud.destroy = MagicMock()

            # Simulate Escape key press
            hud.event_generate("<Escape>")
            hud.update()

            hud.destroy.assert_called_once()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_destroy_cancels_after_callback(self, mock_virtual_mem, mock_cpu):
        mock_cpu.return_value = 10.0
        mock_mem = MagicMock()
        mock_mem.percent = 10.0
        mock_virtual_mem.return_value = mock_mem

        hud = None
        # Verify after_cancel is called when hud is destroyed
        with patch.object(ctk.CTk, "after", return_value="after_job_to_cancel"):
            with patch.object(ctk.CTk, "after_cancel") as mock_after_cancel:
                hud = dashboard.create_dashboard()
                self.assertEqual(hud._after_id, "after_job_to_cancel")

                # Calling destroy should invoke after_cancel
                hud.destroy()
                mock_after_cancel.assert_called_with("after_job_to_cancel")
                self.assertIsNone(hud._after_id)


if __name__ == "__main__":
    unittest.main()
