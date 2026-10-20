#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import time
from instagrapi import Client
from instagrapi.exceptions import (
    RateLimitError,
    PleaseWaitFewMinutes,
    ChallengeRequired,
    ClientForbiddenError,
    LoginRequired,
)

# ======================== CONFIG ========================
# 👇 YAHAN APNI SESSION ID PASTE KARO 👇
SESSION_ID = "36787930739%3AgrQ6LDtBHIzUpU%3A21%3AAYmJsPYZ03H064HC-tgq5XyA02JTVmKntEGDSE9KqA"

# 👇 YAHAN APNI THREAD ID (GC LINK KA NUMBER) PASTE KARO 👇
THREAD_ID = "340282366841710301281152668292958323297" 

MESSAGE_TEMPLATE = """#Oblivion cud ❤️




















#Oblivion cud ❤️




















#Oblivion cud ❤️"""

MAX_RETRIES = 10

# Device rotation list (kept for future password-login, but not used with sessionid)
DEVICE_ROTATION = [
    {
        "app_version": "269.0.0.18.75",
        "android_version": 26,
        "android_release": "8.0.0",
        "dpi": "420dpi",
        "resolution": "1080x1920",
        "manufacturer": "OnePlus",
        "device": "ONEPLUS A3010",
        "model": "ONEPLUS A3010",
        "version_code": "269.0.0.18.75",
    },
    {
        "app_version": "270.0.0.20.85",
        "android_version": 28,
        "android_release": "9.0.0",
        "dpi": "440dpi",
        "resolution": "1080x2280",
        "manufacturer": "Samsung",
        "device": "SM-G973F",
        "model": "SM-G973F",
        "version_code": "270.0.0.20.85",
    }
]

# ======================== HELPERS ========================
def create_client(session_id):
    """Create client and login using session ID (no device settings to avoid mismatch)."""
    cl = Client()
    try:
        cl.login_by_sessionid(session_id)
        print("✅ Logged in using session ID.")
        return cl, True
    except Exception as e:
        print(f"❌ Session ID login failed: {e}")
        return None, False

def send_message_with_retry(client, thread_id, message):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client.direct_send(message, thread_ids=[thread_id])
            print(f"✅ Sent: '{message[:50]}...'")
            return True
        except RateLimitError:
            wait = 120 * attempt
            print(f"⚠️ Rate limit – wait {wait}s ({attempt}/{MAX_RETRIES})")
            time.sleep(wait)
        except PleaseWaitFewMinutes:
            wait = 600
            print(f"⏳ Please wait – wait {wait}s")
            time.sleep(wait)
        except ChallengeRequired:
            print("🔒 Challenge – pausing 1 hour")
            time.sleep(3600)
        except (ClientForbiddenError, LoginRequired):
            print("🔐 Login issue – you need a fresh sessionid.")
            sys.exit("[!] Session expired. Please restart with a new sessionid.")
        except Exception as e:
            wait = 60 * attempt
            print(f"❌ Unknown: {e} – wait {wait}s")
            time.sleep(wait)
    print("❌ Max retries – skipping message")
    return False

def generate_random_band():
    """Generate a random delay band: min 30-50, spread 8-13 seconds."""
    min_delay = random.uniform(30, 50)
    spread = random.uniform(8, 13)
    max_delay = min_delay + spread
    return (min_delay, max_delay)

# ======================== MAIN LOOP ========================
def main():
    # Check if session ID and thread ID are set
    if not SESSION_ID or SESSION_ID == "yahan_apni_session_id_paste_karo":
        sys.exit("[!] Please open the code and paste your session ID in the SESSION_ID variable at the top.")
    
    if not THREAD_ID or THREAD_ID == "yahan_thread_id_paste_karo":
        sys.exit("[!] Please open the code and paste your Thread ID in the THREAD_ID variable at the top.")

    # Create client and login
    client, ok = create_client(SESSION_ID)
    if not ok:
        sys.exit("[!] Initial login failed. Exiting.")

    thread_id = THREAD_ID

    # ---------- Generate initial random band ----------
    current_band = generate_random_band()
    last_band_change = time.time()
    band_interval = random.uniform(2*3600, 3*3600)   # 2-3 hours

    device_index = 0
    last_device_change = time.time()
    device_interval = random.uniform(2*86400, 3*86400)

    # Extra break every 1-2 hours
    last_break_time = time.time()
    break_interval = random.uniform(3600, 7200)

    msg_count = 0
    print(f"🚀 Started – initial band: {current_band[0]:.1f}-{current_band[1]:.1f}s")
    print(f"📨 Sending to thread: {thread_id}")

    while True:
        try:
            # ---------- LOGIC 1: Random number ----------
            num = random.randint(1, 10**10)
            if random.choice([True, False]):
                full_msg = f"{num} {MESSAGE_TEMPLATE}"
            else:
                full_msg = f"{MESSAGE_TEMPLATE} {num}"

            # Send with retry
            if send_message_with_retry(client, thread_id, full_msg):
                msg_count += 1
                print(f"📊 Total sent: {msg_count}")

            # ---------- LOGIC 2: Delay from current band ----------
            delay = random.uniform(current_band[0], current_band[1])
            print(f"⏱️ Waiting {delay:.2f}s (band: {current_band[0]:.1f}-{current_band[1]:.1f}s)")
            time.sleep(delay)

            # ---------- Band rotation (every 2-3 hours) ----------
            if time.time() - last_band_change >= band_interval:
                current_band = generate_random_band()
                last_band_change = time.time()
                band_interval = random.uniform(2*3600, 3*3600)
                print(f"🔄 New random band: {current_band[0]:.1f}-{current_band[1]:.1f}s")

            # ---------- LOGIC 3: Device rotation (2-3 days) ----------
            if time.time() - last_device_change >= device_interval:
                print("⏳ Device rotation would happen, but sessionid login cannot change device.")
                last_device_change = time.time()
                device_interval = random.uniform(2*86400, 3*86400)

            # ---------- Extra break every 1-2 hours ----------
            if time.time() - last_break_time >= break_interval:
                extra = random.uniform(60, 180)   # 1-3 minutes
                print(f"☕ Extra break: {extra:.0f}s")
                time.sleep(extra)
                last_break_time = time.time()
                break_interval = random.uniform(3600, 7200)

        except KeyboardInterrupt:
            print("🛑 Stopped by user")
            break
        except Exception as e:
            print(f"💥 Main loop crash: {e} – restarting in 60s")
            time.sleep(60)
            continue

if __name__ == "__main__":
    main()
