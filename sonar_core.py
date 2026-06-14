import psutil
import time
import requests
import os

print("SONAR-X Core initialized. Listening to the system pulse...")

def alert_desktop(message):
    # Triggers a native macOS Ventura notification banner with a sound!
    apple_script = f'display notification "{message}" with title "Project SONAR-X" sound name "Glass"'
    os.system(f"osascript -e '{apple_script}'")

def trigger_vdj(vdj_script):
    # This pings the Virtual DJ Network Control Plugin locally.
    url = f"http://127.0.0.1:80/execute?script={vdj_script}"
    try:
        # A quick 1-second timeout so the agent doesn't freeze if VDJ is closed
        requests.get(url, timeout=1) 
    except Exception:
        pass # If VDJ is offline, the agent just keeps dancing

while True:
    # Get the CPU percentage over a 2-second window
    cpu_load = psutil.cpu_percent(interval=2)
    # Check the RAM percentage
    ram_load = psutil.virtual_memory().percent
    
    print(f"[Heartbeat] CPU: {cpu_load}% | RAM: {ram_load}%")

    # If the CPU hits 85%, the system is struggling!
    if cpu_load > 85.0:
        alert_msg = f"CPU hitting {cpu_load}%. Cooling down the mix!"
        print(f"ALERT: {alert_msg}")
        
        # 1. Pop up a silent Ventura notification
        alert_desktop(alert_msg)
        
        # 2. Tell VDJ to trigger pad 1 (maybe an airhorn!) and drop the volume to 80%
        trigger_vdj("sampler_pad 1 play & volume 80%")
        
        # Sleep for 15 seconds to let the system breathe before alerting again
        time.sleep(15)

