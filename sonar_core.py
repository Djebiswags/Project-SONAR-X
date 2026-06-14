import psutil
import time
import os

print("SONAR-X Core initialized. Listening to the system pulse...")

def alert_desktop(message):
    # Sends a notification to your screen
    apple_script = f'display notification "{message}" with title "Project SONAR-X"'
    os.system(f"osascript -e '{apple_script}'")

def check_ram_cool_down():
    # Monitors RAM and alerts if it gets "too hot" (80%)
    ram_usage = psutil.virtual_memory().percent
    if ram_usage > 80.0:
        alert_desktop(f"Warning: RAM usage at {ram_usage}%. Sentinel is monitoring processes.")
        # We will add process-killing logic here once we build the 'Kill List'
    return ram_usage

def check_network():
    # Simple check: sends a small packet to see if the network is alive
    try:
        # We'll use a fast ping check here later
        return "Connected"
    except:
        return "Obstruction Detected"

while True:
    cpu_load = psutil.cpu_percent(interval=2)
    ram_load = check_ram_cool_down()
    net_status = check_network()

    print(f"[Sentinel Pulse] CPU: {cpu_load}% | RAM: {ram_load}% | Network: {net_status}")
    
    time.sleep(5) # Keeps the Sentinel's eyes open every 5 seconds
