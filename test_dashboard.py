import unittest
from unittest.mock import patch

# We can patch psutil before importing or within the tests
with (
    patch("psutil.cpu_percent", return_value=15.0),
    patch("psutil.virtual_memory") as mock_vm,
):
    mock_vm.return_value.percent = 45.0
    from dashboard import create_dashboard


class TestSonarHUD(unittest.TestCase):
    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_creation_and_telemetry_safe(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_vm.return_value.percent = 45.0

        hud = create_dashboard()
        self.assertIsNotNone(hud)

        # Verify the title and default settings
        self.assertEqual(hud.title(), "SONAR-X | Live Telemetry")

        # Force updates to ensure GUI elements process
        hud.update()

        # Check safe status text (CPU < 80)
        self.assertIn("🟢", hud.cpu_label.cget("text"))
        self.assertIn("15.0%", hud.cpu_label.cget("text"))
        self.assertIn("🟢", hud.ram_label.cget("text"))
        self.assertIn("45.0%", hud.ram_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_hud_creation_and_telemetry_warning(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 85.0
        mock_vm.return_value.percent = 75.0

        hud = create_dashboard()
        hud.update()

        # Check alert status text (CPU > 80)
        self.assertIn("🚨", hud.cpu_label.cget("text"))
        self.assertIn("85.0%", hud.cpu_label.cget("text"))

        hud.destroy()

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_escape_key_closes_hud(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_vm.return_value.percent = 45.0

        hud = create_dashboard()
        hud.deiconify()
        hud.focus_force()
        hud.update()

        # Track if destroy gets called
        destroy_called = False
        original_destroy = hud.destroy

        def mock_destroy():
            nonlocal destroy_called
            destroy_called = True
            original_destroy()

        hud.destroy = mock_destroy

        # Trigger Escape key press
        hud.event_generate("<Escape>")
        hud.update()

        self.assertTrue(destroy_called)

    @patch("psutil.cpu_percent")
    @patch("psutil.virtual_memory")
    def test_cleanup_after_loop_on_destroy(self, mock_vm, mock_cpu):
        mock_cpu.return_value = 15.0
        mock_vm.return_value.percent = 45.0

        hud = create_dashboard()
        hud.update()

        self.assertIsNotNone(hud._update_job_id)

        # Destroy HUD
        hud.destroy()

        # Job ID should be set to None
        self.assertIsNone(hud._update_job_id)


if __name__ == "__main__":
    unittest.main()
