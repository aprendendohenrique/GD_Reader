import struct


class DataBuffer:
    """Sequential binary reader."""

    def __init__(self, data: bytes):
        self.data = data
        self.cursor = 0

    @property
    def length(self):
        return len(self.data)

    def eof(self):
        return self.cursor >= self.length

    def read_bytes(self, amount: int) -> bytes:
        if self.cursor + amount > self.length:
            raise EOFError("End of file reached")

        value = self.data[self.cursor:self.cursor + amount]
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