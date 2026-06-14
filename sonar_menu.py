import rumps
import psutil
import requests
import os
import threading
import time
from pynput import keyboard

class SonarXApp(rumps.App):
    def __init__(self):
        super(SonarXApp, self).__init__("🎧 SONAR-X")
        self.monitoring = False
        self.is_cooling = False
        threading.Thread(target=self.start_macro_listener, daemon=True).start()

    def start_macro_listener(self):
        def on_activate_epic_macro():
            self.alert_desktop("🌊 MACRO: Phantom Echo Out Initiated!")
            self.trigger_vdj("deck active loop 8 & deck active effect 'echo' active on & deck 
active volume 0% gradually 4000ms")
        
        with keyboard.GlobalHotKeys({'<cmd>+<shift>+m': on_activate_epic_macro}) as h:
            h.join()

    @rumps.clicked("▶️ Start / Stop Monitoring")
    def toggle_monitoring(self, _):
        self.monitoring = not self.monitoring
        if self.monitoring:
            threading.Thread(target=self.heartbeat_loop, daemon=True).start()
            rumps.notification("SONAR-X", "Agent Online", "Defensive & Network systems active.")
        else:
            self.title = "🎧 SONAR-X"
            self.is_cooling = False
            rumps.notification("SONAR-X", "Agent Offline", "Standing down.")

    def check_network_status(self):
        try:
            requests.get("https://www.google.com", timeout=2)
            return "🟢"
        except:
            self.alert_desktop("NETWORK OBSTRUCTION: Sentinel detected connection loss!")
            return "🔴"

    def heartbeat_loop(self):
        while self.monitoring:
            cpu_load = psutil.cpu_percent(interval=2)
            net_icon = self.check_network_status()
            
            if self.is_cooling:
                self.title = f"❄️ COOLING: {cpu_load}% | Net: {net_icon}"
                if cpu_load < 60.0:
                    self.is_cooling = False
                    self.alert_desktop("System stable. Resuming operations.")
            else:
                if cpu_load > 85.0:
                    self.is_cooling = True
                    self.alert_desktop(f"REDLINE: {cpu_load}%! Engaging cooling protocol.")
                    self.trigger_vdj("volume 80%")
                
                self.title = f"🎧 CPU: {cpu_load}% | Net: {net_icon}"
            
            time.sleep(5) # Breathes every 5 seconds

    def alert_desktop(self, message):
        apple_script = f'display notification "{message}" with title "Project SONAR-X" sound name 
"Glass"'
        os.system(f"osascript -e '{apple_script}'")

    def trigger_vdj(self, vdj_script):
        try:
            requests.get("http://127.0.0.1:80/execute", params={"script": vdj_script}, timeout=1)
        except Exception:
            pass

if __name__ == "__main__":
    SonarXApp().run()
