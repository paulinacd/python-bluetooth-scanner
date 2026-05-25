from bleak import BleakScanner
import asyncio
from datetime import datetime
import csv

LOG_FILE = "C:/Users/paucd/OneDrive/Documents/bluetooth_log.csv"

seen_devices = set()

async def scan_loop():
    with open(LOG_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Event", "Device Name", "MAC Address"])

    print("Bluetooth Proximity Logger Running...")
    print("Press Ctrl + C to stop.\n")

    while True:
        print("Scanning...\n")
        devices = await BleakScanner.discover(timeout=5.0)

        current_devices = set()

        for device in devices:
            name = device.name if device.name else "Unknown Device"
            address = device.address
            current_devices.add(address)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if address not in seen_devices:
                print(f"NEW DEVICE FOUND: {name} | {address} | {timestamp}")

                with open(LOG_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, "Device Appeared", name, address])

        for old_device in seen_devices:
            if old_device not in current_devices:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"DEVICE LEFT RANGE: {old_device} | {timestamp}")

                with open(LOG_FILE, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([timestamp, "Device Left Range", "Unknown", old_device])

        seen_devices.clear()
        seen_devices.update(current_devices)

        print("-" * 50)
        await asyncio.sleep(3)

try:
    asyncio.run(scan_loop())
except KeyboardInterrupt:
    print("\nScanner stopped. Log saved to bluetooth_log.csv.")