import struct


class DataBuffer:
    """Sequential binary reader."""

    def __init__(self, data: bytes):
        self.bytes = data
        self.cursor = 0

    @property
    def length(self):
        return len(self.bytes)

    def eof(self):
        return self.cursor >= self.length

    def read_bytes(self, amount: int) -> bytes:
        if self.cursor + amount > self.length:
            raise EOFError("End of file reached")

        value = self.bytes[self.cursor:self.cursor + amount]
        self.cursor += amount
        return value

    def read_uint(self):
        return struct.unpack("<I", self.read_bytes(4))[0]

    def read_int(self):
        return struct.unpack("<i", self.read_bytes(4))[0]

    def read_float(self):
        return struct.unpack("<f", self.read_bytes(4))[0]

    def read_byte(self):
        return self.read_bytes(1)[0]

    def peek(self, n=32):
        return self.bytes[self.cursor:self.cursor + n]

    def scan_uints(self, n=10):
        pos = self.cursor
        vals = []

        for _ in range(n):
            vals.append(self.read_uint())

        self.cursor = pos
        return vals

    def debug_stream(self, n=10):
        pos = self.cursor

        print("DEBUG STREAM:")

        for i in range(n):
            val = self.read_uint()
            print(i, hex(val))

        self.cursor = pos