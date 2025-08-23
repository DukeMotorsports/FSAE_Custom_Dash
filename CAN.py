import can
import json
import time

def parse_can_id(id_val):
    """Convert CAN ID from JSON (supports int, decimal string, hex string with/without 0x)."""
    if isinstance(id_val, int):
        return id_val
    if isinstance(id_val, str):
        id_val = id_val.strip()
        # If it's already prefixed with "0x", parse as hex
        if id_val.lower().startswith("0x"):
            return int(id_val, 16)
        # If it looks like hex (has letters A-F), force hex
        if any(c in "abcdefABCDEF" for c in id_val):
            return int(id_val, 16)
        # Otherwise assume decimal
        return int(id_val)
    raise ValueError(f"Unsupported CAN ID format: {id_val}")

class CANDecoder:
    def __init__(self, json_file, port="COM3", bitrate=1000000):
        # Load JSON definitions
        with open(json_file, "r") as f:
            signal_definitions = json.load(f)

        # Build quick lookup
        self.signal_map = {}
        for sig in signal_definitions:
            can_id = parse_can_id(sig["id"])
            if can_id not in self.signal_map:
                self.signal_map[can_id] = []
            self.signal_map[can_id].append(sig)

        # Setup CAN bus
        self.bus = can.interface.Bus(interface="slcan", channel=port, bitrate=bitrate)

    def decode_signal(self, sig, data):
        offset = sig["offset"]
        length = sig.get("base_resolution", 1)
        if offset + length > len(data):
            return None

        raw_bytes = data[offset:offset+length]
        raw_val = int.from_bytes(raw_bytes, byteorder="little", signed=False)

        # Apply scaling
        multiplier = sig.get("multiplier", 1)
        divisor = sig.get("divisor", 1)
        adder = sig.get("adder", 0)
        baseResolution = sig.get("resolution", 1)

        return ((raw_val * baseResolution * multiplier) / divisor) + adder

    def decode_message(self, msg):
        """Return dict of decoded signals for this CAN msg."""
        decoded = {}
        if msg.arbitration_id in self.signal_map:
            for sig in self.signal_map[msg.arbitration_id]:
                val = self.decode_signal(sig, msg.data)
                if val is not None:
                    decoded[sig.get("name", f"id_{msg.arbitration_id}")] = val
        return decoded

    def listen(self, callback=None, timeout=1.0):
        """
        Blocking loop: listen for CAN messages.
        Always prints raw frames.
        Calls callback(decoded_dict) for each decoded message.
        """
        print("Listening for CAN messages...")
        try:
            while True:
                msg = self.bus.recv(timeout=timeout)
                if msg is None:
                    continue

                # Always show raw message
                # print(f"RAW ID: {msg.arbitration_id:#04x}  Data: {msg.data.hex()}")

                # Decode if JSON has a match
                decoded = self.decode_message(msg)
                if decoded:
                    _latest_values.update(decoded)
                    
                    print("  Decoded:", decoded)
                    if callback:
                        callback(decoded)
        except KeyboardInterrupt:
            print("\nStopped listening.")
        finally:
            self.bus.shutdown()

# --- Global cache for latest values ---
_latest_values = {}

def get_rpm(default=0):
    """Getter for latest RPM value (returns default if not yet seen)."""
    return _latest_values.get("RPM", default)