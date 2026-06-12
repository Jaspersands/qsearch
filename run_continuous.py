import time
import subprocess
import sys

print("==================================================")
# Print details about continuous running
print("Starting Continuous Quantum Algorithm Search Loop")
print("Press Ctrl+C to stop at any time.")
print("==================================================")

while True:
    print(f"\n--- Starting Search Run at {time.strftime('%Y-%m-%d %H:%M:%S')} ---")
    try:
        # Run discover_algorithms.py as an independent subprocess
        # Using sys.executable ensures it uses the same python environment
        subprocess.run([sys.executable, "-u", "discover_algorithms.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Search run finished with an error: {e}")
    except KeyboardInterrupt:
        print("\nExiting search loop...")
        break
        
    print("\nWaiting 2 minutes before starting the next search...")
    try:
        time.sleep(120)
    except KeyboardInterrupt:
        print("\nExiting search loop...")
        break
