import rumps
import psutil
import requests
import os
import threading
import time
import json
import sys
import subprocess

class SonarXApp(rumps.App):
    def __init__(self):
        # Initialize the app with the base title
        super(SonarXApp, self).__init__("🎧 SONAR-X")
        self.monitoring = False
        self.is_cooling = False
        self.kill_list = self.load_config()

    def load_config(self):
        # Pulls the hit-list from config.json
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                return data.get("kill_list", [])
        except Exception:
            return []

    @rumps.clicked("▶️ Start / Stop Sentinel")
    def toggle_monitoring(self, _):
        # Toggles the main defensive loop
        self.monitoring = not self.monitoring
        if self.monitoring:
            threading.Thread(target=self.heartbeat_loop, daemon=True).start()
            rumps.notification("SONAR-X", "Agent Online", "Defensive systems active.")
        else:
            self.title = "🎧 SONAR-X"
            self.is_cooling = False
            rumps.notification("SONAR-X", "Agent Offline", "Standing down.")

    @rumps.clicked("📊 Launch Visual HUD")
    def open_dashboard(self, _):
        # Use the full path to ensure the HUD can find its own environment
        subprocess.Popen(["/Users/oracle/agent_env/bin/python3", "/Users/oracle/Project-SONAR-X/dashboard.py"])

    def execute_silent_kill(self):
        # The Silent Assassin Logic
        killed_count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] in self.kill_list:
                    proc.terminate()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return killed_count

    def check_network_status(self):
        # Pings the outside world to check connectivity
        try:
            requests.get("https://www.google.com", timeout=2)
            return "🟢"
        except:
            return "🔴"

    def heartbeat_loop(self):
        # The core engine that breathes every 5 seconds
        while self.monitoring:
            cpu_load = psutil.cpu_percent(interval=2)
            net_icon = self.check_network_status()
            
            if self.is_cooling:
                self.title = f"❄️ COOLING: {cpu_load}% | {net_icon}"
                if cpu_load < 60.0:
                    self.is_cooling = False
                    
                    # Short variable to prevent terminal cut-off
                    stable_msg = "System stable. Resuming standard operations."
                    self.alert_desktop(stable_msg)
            else:
                if cpu_load > 85.0:
                    self.is_cooling = True
                    assassinations = self.execute_silent_kill()
                    
                    # Short variable to prevent terminal cut-off
                    warn_msg = f"REDLINE! Terminated {assassinations} background hogs."
                    self.alert_desktop(warn_msg)
                
                self.title = f"🎧 CPU: {cpu_load}% | {net_icon}"
            
            time.sleep(5)

    def alert_desktop(self, message):
        # Safely split AppleScript across multiple lines to avoid syntax breaks
        part_one = f'display notification "{message}" '
        part_two = 'with title "Project SONAR-X" sound name "Glass"'
        full_script = part_one + part_two
        
        os.system(f"osascript -e '{full_script}'")

if __name__ == "__main__":
    SonarXApp().run()
