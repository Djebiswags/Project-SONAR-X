import tkinter as tk
from unittest.mock import patch

import pytest

pytest.importorskip("customtkinter")

import dashboard


def test_dashboard_creation_and_telemetry_normal_load():
    with patch.object(dashboard.psutil, "cpu_percent", return_value=35.0), patch.object(
        dashboard.psutil, "virtual_memory"
    ) as mock_vm:
        mock_vm.return_value.percent = 50.0
        hud = dashboard.create_dashboard()

        try:
            assert "🟢 CPU Load: 35.0%" in hud.cpu_label.cget("text")
            assert "RAM Usage: 50.0%" in hud.ram_label.cget("text")
            assert hud.cpu_label.cget("text_color") == "#00FFCC"
        finally:
            hud.destroy()


def test_dashboard_telemetry_high_load():
    with patch.object(dashboard.psutil, "cpu_percent", return_value=88.5), patch.object(
        dashboard.psutil, "virtual_memory"
    ) as mock_vm:
        mock_vm.return_value.percent = 75.0
        hud = dashboard.create_dashboard()

        try:
            assert "🚨 CPU Load: 88.5%" in hud.cpu_label.cget("text")
            assert "RAM Usage: 75.0%" in hud.ram_label.cget("text")
            assert hud.cpu_label.cget("text_color") == "#FF3333"
        finally:
            hud.destroy()


def test_dashboard_escape_key_closes_window():
    with patch.object(dashboard.psutil, "cpu_percent", return_value=10.0), patch.object(
        dashboard.psutil, "virtual_memory"
    ) as mock_vm:
        mock_vm.return_value.percent = 20.0
        hud = dashboard.create_dashboard()

        try:
            hud.deiconify()
            hud.focus_force()
            hud.update()
            hud.event_generate("<Escape>")
            hud.update()
            is_alive = True
            try:
                is_alive = bool(hud.winfo_exists())
            except (tk.TclError, AttributeError):
                is_alive = False
            assert not is_alive
        finally:
            try:
                if hud.winfo_exists():
                    hud.destroy()
            except (tk.TclError, AttributeError):
                pass
