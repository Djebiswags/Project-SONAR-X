import argparse
import json
import os
import time
from pathlib import Path

import psutil
import requests


CONFIG_FILE = Path(__file__).with_name("config.json")
DEFAULT_CPU_THRESHOLD = 85.0
DEFAULT_RAM_THRESHOLD = 80.0
DEFAULT_CPU_INTERVAL = 2.0
DEFAULT_SLEEP_INTERVAL = 5.0


def alert_desktop(message: str) -> None:
    """Send a macOS notification to the user."""
    safe_message = message.replace('"', '\\"')
    apple_script = f'display notification "{safe_message}" with title "Project SONAR-X" sound name "Glass"'
    os.system(f"osascript -e '{apple_script}'")


def load_config(path: Path = CONFIG_FILE) -> list[str]:
    """Load the local kill list from config.json."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        return data.get("kill_list", []) if isinstance(data, dict) else []
    except json.JSONDecodeError:
        return []


def check_ram_usage(threshold: float = DEFAULT_RAM_THRESHOLD) -> float:
    """Return RAM usage and alert if the value exceeds the threshold."""
    ram_usage = psutil.virtual_memory().percent
    if ram_usage > threshold:
        alert_desktop(f"Warning: RAM usage at {ram_usage}%. Sentinel is monitoring processes.")
    return ram_usage


def check_network() -> str:
    """Return connection status by checking a known public endpoint."""
    try:
        requests.get("https://www.google.com", timeout=2)
        return "Connected"
    except requests.RequestException:
        return "Disconnected"


def execute_silent_kill(kill_list: list[str]) -> int:
    """Terminate any matching background process names in the kill list."""
    killed_count = 0
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info.get("name") in kill_list:
                proc.terminate()
                killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return killed_count


def run_cycle(
    kill_list: list[str],
    cpu_threshold: float = DEFAULT_CPU_THRESHOLD,
    ram_threshold: float = DEFAULT_RAM_THRESHOLD,
    cpu_interval: float = DEFAULT_CPU_INTERVAL,
    sleep_interval: float = DEFAULT_SLEEP_INTERVAL,
) -> tuple[float, float, str]:
    """Run a single monitoring cycle and return the observed telemetry."""
    cpu_load = psutil.cpu_percent(interval=cpu_interval)
    ram_load = check_ram_usage(ram_threshold)
    net_status = check_network()

    if cpu_load > cpu_threshold and kill_list:
        terminated = execute_silent_kill(kill_list)
        alert_desktop(f"High CPU detected: {cpu_load}%. Terminated {terminated} background process(es).")

    print(f"[Sentinel Pulse] CPU: {cpu_load}% | RAM: {ram_load}% | Network: {net_status}")
    time.sleep(sleep_interval)
    return cpu_load, ram_load, net_status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Project SONAR-X system sentinel")
    parser.add_argument("--once", action="store_true", help="Run a single monitoring cycle and exit")
    parser.add_argument("--cpu-threshold", type=float, default=DEFAULT_CPU_THRESHOLD, help="CPU threshold to trigger mitigation")
    parser.add_argument("--ram-threshold", type=float, default=DEFAULT_RAM_THRESHOLD, help="RAM threshold to trigger alerts")
    parser.add_argument("--cpu-interval", type=float, default=DEFAULT_CPU_INTERVAL, help="CPU sample interval in seconds")
    parser.add_argument("--sleep-interval", type=float, default=DEFAULT_SLEEP_INTERVAL, help="Sleep time between cycles in seconds")
    return parser.parse_args()


def main() -> None:
    print("SONAR-X Core initialized. Listening to the system pulse...")
    kill_list = load_config()
    args = parse_args()

    if args.once:
        run_cycle(
            kill_list=kill_list,
            cpu_threshold=args.cpu_threshold,
            ram_threshold=args.ram_threshold,
            cpu_interval=args.cpu_interval,
            sleep_interval=0,
        )
        return

    while True:
        run_cycle(
            kill_list=kill_list,
            cpu_threshold=args.cpu_threshold,
            ram_threshold=args.ram_threshold,
            cpu_interval=args.cpu_interval,
            sleep_interval=args.sleep_interval,
        )


if __name__ == "__main__":
    main()
