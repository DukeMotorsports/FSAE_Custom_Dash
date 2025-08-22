from CAN import CANDecoder

WATCH_SIGNALS = ["oil pres"]


if __name__ == "__main__":
    decoder = CANDecoder("can_signals.json", port="COM3", bitrate=1000000)
    decoder.listen()
