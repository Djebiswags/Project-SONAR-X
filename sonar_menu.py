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
        
        self.macro_thread = threading.Thread(target=self.start_macro_listener, daemon=True)
        self.macro_thread.start()

    def start_macro_listener(self):
        def on_activate_epic_macro():
            self.alert_desktop("🌊 MACRO: Phantom Echo Out Initiated!")
            self.trigger_vdj("deck active loop 8 & deck active effect 'echo' active on & deck active volume 0% gradually 4000ms")

        with keyboard.GlobalHotKeys({'<cmd>+<shift>+m': on_activate_epic_macro}) as h:
            h.join()

    @rumps.clicked("▶️ Start / Stop Monitoring")
    def toggle_monitoring(self, _):
        self.monitoring = not self.monitoring
        if self.monitoring:
            threading.Thread(target=self.heartbeat_loop, daemon=True).start()
            rumps.notification("SONAR-X", "Agent Online", "Defensive & Offensive systems active.")
        else:
            self.title = "🎧 SONAR-X"
            self.is_cooling = False
            rumps.notification("SONAR-X", "Agent Offline", "Standing down.")

    def heartbeat_loop(self):
        while self.monitoring:
            cpu_load = psutil.cpu_percent(interval=2)
            
            if self.is_cooling:
                self.title = f"❄️ COOLING: {cpu_load}%"
                if cpu_load < 60.0:
                    self.is_cooling = False
                    self.alert_desktop("System stable. Resuming operations.")
            else:
                bpm_alert = self.check_bpm_clash()
                
                if bpm_alert:
                    self.title = f"⚠️ BPM CLASH | CPU: {cpu_load}%"
                else:
                    self.title = f"🎧 CPU: {cpu_load}%"
                    
                if cpu_load > 85.0:
                    self.is_cooling = True
                    self.alert_desktop(f"REDLINE: {cpu_load}%! Engaging cooling protocol.")
                    self.trigger_vdj("volume 80%")
                    
            time.sleep(2)

    def check_bpm_clash(self):
        try:
            url1 = "http://127.0.0.1:80/query"
            url2 = "http://127.0.0.1:80/query"
            # Passing the script via the 'params' dictionary automatically fixes the Ampersand Collision!
            bpm1 = float(requests.get(url1, params={"script": "deck 1 get_bpm"}, timeout=1).text)
            bpm2 = float(requests.get(url2, params={"script": "deck 2 get_bpm"}, timeout=1).text)
            
            if bpm1 > 0 and bpm2 > 0 and abs(bpm1 - bpm2) > 10:
                return True
        except Exception:
            pass
        return False

    def alert_desktop(self, message):
        apple_script = f'display notification "{message}" with title "Project SONAR-X" sound name "Glass"'
        os.system(f"osascript -e '{apple_script}'")

    def trigger_vdj(self, vdj_script):
        url = "http://127.0.0.1:80/execute"
        try:
            # The 'params' dictionary perfectly encodes all spaces and '&' symbols for the network
            requests.get(url, params={"script": vdj_script}, timeout=1) 
        except Exception:
            pass 

if __name__ == "__main__":
    SonarXApp().run()
