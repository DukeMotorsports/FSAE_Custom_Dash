import can

# Update COM3 to match your device’s port in Device Manager
bus = can.interface.Bus(interface="slcan", channel="COM3", bitrate=1000000)

print("Listening for CAN messages from MoTeC M150...")

try:
    while True:
        msg = bus.recv(timeout=1.0)  # waits up to 1 second
        if msg is not None:
            print(f"ID: {msg.arbitration_id:#04x}  Data: {msg.data.hex()} DLC:{msg.dlc}")
except KeyboardInterrupt:
    print("\nStopped listening.")
