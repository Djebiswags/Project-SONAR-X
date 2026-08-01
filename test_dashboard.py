import unittest

# Force headless / mock tkinter if needed, or use real customtkinter under xvfb
from dashboard import create_dashboard

class TestSonarHUD(unittest.TestCase):
    def setUp(self):
        # We can construct the dashboard inside xvfb
        self.hud = create_dashboard()

    def tearDown(self):
        try:
            self.hud.destroy()
        except Exception:
            pass

    def test_initialization(self):
        """Test that the HUD initializes with correctly configured labels."""
        self.hud.update()
        self.assertIn("CPU Load", self.hud.cpu_label.cget("text"))
        self.assertIn("RAM Usage", self.hud.ram_label.cget("text"))

    def test_escape_key_binding(self):
        """Test that the Escape key closes the window."""
        self.hud.deiconify()
        self.hud.focus_force()
        self.hud.update()

        # Verify it has update_job
        self.assertIsNotNone(self.hud.update_job)

        # Trigger <Escape> key event
        try:
            self.hud.event_generate("<Escape>")
            if self.hud.winfo_exists():
                self.hud.update()
        except Exception:
            pass

        # Check that update_job is canceled and set to None
        self.assertIsNone(self.hud.update_job)

if __name__ == "__main__":
    unittest.main()
