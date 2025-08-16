import can

# Replace "COM3" with your actual COM port
bus = can.interface.Bus(interface="slcan", channel="COM3", bitrate=500000)

print("Listening for CAN messages...")
while True:
    msg = bus.recv()
    if msg:
        print(f"ID: {msg.arbitration_id:#04x}  Data: {msg.data.hex()}")
