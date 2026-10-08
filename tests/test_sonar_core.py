"""Unit tests for sonar_core.py — the SONAR-X pulse engine.

Run:  python -m pytest tests/ -v
"""
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

import sonar_core


# ---------------------------------------------------------------- load_config


def test_load_config_missing_file_returns_empty(tmp_path):
    assert sonar_core.load_config(tmp_path / "nope.json") == []


def test_load_config_reads_kill_list(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"kill_list": ["Spotify", "Dropbox"]}))
    assert sonar_core.load_config(cfg) == ["Spotify", "Dropbox"]


def test_load_config_malformed_json_returns_empty(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text("{not valid json")
    assert sonar_core.load_config(cfg) == []


def test_load_config_non_dict_returns_empty(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps(["just", "a", "list"]))
    assert sonar_core.load_config(cfg) == []


def test_load_config_missing_kill_list_key_returns_empty(tmp_path):
    cfg = tmp_path / "config.json"
    cfg.write_text(json.dumps({"other_key": 1}))
    assert sonar_core.load_config(cfg) == []


# ------------------------------------------------------------ check_ram_usage


def _fake_virtual_memory(percent):
    vm = Mock()
    vm.percent = percent
    return vm


def test_check_ram_usage_returns_percent_and_stays_quiet_below_threshold():
    with patch.object(
        sonar_core.psutil, "virtual_memory", return_value=_fake_virtual_memory(42.0)
    ), patch.object(sonar_core, "alert_desktop") as alert:
        assert sonar_core.check_ram_usage(threshold=80.0) == 42.0
        alert.assert_not_called()


def test_check_ram_usage_alerts_above_threshold():
    with patch.object(
        sonar_core.psutil, "virtual_memory", return_value=_fake_virtual_memory(95.0)
    ), patch.object(sonar_core, "alert_desktop") as alert:
        assert sonar_core.check_ram_usage(threshold=80.0) == 95.0
        alert.assert_called_once()


# --------------------------------------------------------- execute_silent_kill


class _FakeProc:
    def __init__(self, name, terminate=None):
        self.info = {"name": name}
        self.terminate = Mock(side_effect=terminate) if terminate else Mock()


def test_execute_silent_kill_terminates_only_listed_processes():
    procs = [_FakeProc("Spotify"), _FakeProc("Finder"), _FakeProc("Dropbox")]
    with patch.object(sonar_core.psutil, "process_iter", return_value=iter(procs)):
        killed = sonar_core.execute_silent_kill(["Spotify", "Dropbox"])
    assert killed == 2
    procs[0].terminate.assert_called_once()
    procs[1].terminate.assert_not_called()
    procs[2].terminate.assert_called_once()


def test_execute_silent_kill_skips_vanished_or_denied_processes():
    import psutil as real_psutil

    gone = _FakeProc("Spotify", terminate=real_psutil.NoSuchProcess(123))
    denied = _FakeProc("Dropbox", terminate=real_psutil.AccessDenied(456))
    with patch.object(
        sonar_core.psutil, "process_iter", return_value=iter([gone, denied])
    ):
        assert sonar_core.execute_silent_kill(["Spotify", "Dropbox"]) == 0


def test_execute_silent_kill_empty_list_kills_nothing():
    procs = [_FakeProc("Spotify")]
    with patch.object(sonar_core.psutil, "process_iter", return_value=iter(procs)):
        assert sonar_core.execute_silent_kill([]) == 0
    procs[0].terminate.assert_not_called()


# ----------------------------------------------------------------- parse_args


def test_parse_args_once_flag():
    with patch("sys.argv", ["sonar_core.py", "--once"]):
        assert sonar_core.parse_args().once is True


def test_parse_args_defaults():
    with patch("sys.argv", ["sonar_core.py"]):
        args = sonar_core.parse_args()
        assert args.once is False
        assert args.cpu_threshold == sonar_core.DEFAULT_CPU_THRESHOLD
        assert args.ram_threshold == sonar_core.DEFAULT_RAM_THRESHOLD
