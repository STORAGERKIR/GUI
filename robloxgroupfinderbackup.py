import os
import sys
import subprocess
import threading
import requests
import random
import ctypes
import time

def install_module(module_name, package_name=None):
    if package_name is None:
        package_name = module_name
    try:
        __import__(module_name)
        print(f"[✓] {module_name} already installed")
        return True
    except ImportError:
        print(f"[!] Installing {module_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"[✓] Successfully installed {module_name}")
            return True
        except subprocess.CalledProcessError:
            print(f"[X] Failed to install {module_name}")
            return False

def check_dependencies():
    print("\nChecking dependencies...\n")
    
    # First install dhooks properly (the correct package name is 'dhooks-lite')
    if not install_module('dhooks', 'dhooks-lite'):
        return False
    
    # Then check other requirements
    requirements = ['requests']
    for req in requirements:
        if not install_module(req):
            return False
    return True

if not check_dependencies():
    input("\nPress Enter to exit...")
    sys.exit(1)

from dhooks import Webhook

def groupfinder():
    try:
        id = random.randint(1000000, 1150000)
        r = requests.get(f"https://www.roblox.com/groups/group.aspx?gid={id}", timeout=30)
        if 'owned' not in r.text:
            re = requests.get(f"https://groups.roblox.com/v1/groups/{id}", timeout=30)
            if re.status_code != 429:
                if 'errors' not in re.json():
                    if 'isLocked' not in re.text and 'owner' in re.text:
                        if re.json()['publicEntryAllowed'] == True and re.json()['owner'] == None:
                            hook.send(f'Hit: https://www.roblox.com/groups/group.aspx?gid={id}')
                            print(f"[+] Hit: {id}")
                        else:
                            print(f"[-] No Entry Allowed: {id}")
                    else:
                        print(f"[-] Group Locked: {id}")
            else:
                print(f"[-] Rate Limited - Waiting...")
        else:
            print(f"[-] Already Owned: {id}")
    except Exception as e:
        print(f"[-] Error: {str(e)}")

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Roblox Group Finder")
    print("\nRoblox Group Finder")
    print("="*20 + "\n")
    
    try:
        webhook_url = input("[>] Enter webhook URL: ").strip()
        if not webhook_url.startswith('http'):
            raise ValueError("Invalid webhook URL")
            
        threads = int(input("[>] Thread count (recommend 5-10): "))
        if threads < 1 or threads > 50:
            raise ValueError("Thread count must be between 1-50")
            
        global hook
        hook = Webhook(webhook_url)
        
        print("\n[+] Starting search (Press Ctrl+C to stop)...\n")
        
        while True:
            if threading.active_count() <= threads:
                threading.Thread(target=groupfinder).start()
            time.sleep(0.1)
            
    except Exception as e:
        print(f"\n[!] Error: {e}")
    finally:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
