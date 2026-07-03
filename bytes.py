import struct


class DataBuffer:

    def __init__(self, b):
        self.bytes = b
        self.cursor = 0
        self.xor_key = 1431655765
        self.key = None

    def read_bytes(self, pos):
        if self.cursor + pos > len(self.bytes):
            raise EOFError("End of file reached")

        value = self.bytes[self.cursor: self.cursor + pos]
        self.cursor += pos

        return value

    def read_uint(self):
        raw = self.read_bytes(4)
        return struct.unpack("<I", raw)[0]

    def read_int(self):
        raw = self.read_bytes(4)
        return struct.unpack("<i", raw)[0]

    def read_crypto_key(self):
        encrypted_key = self.read_uint()
        self.key = encrypted_key ^ self.xor_key
        # chamar o Generate Table



data = struct.pack("<I", 1000)
buffer = DataBuffer(data)
print(buffer.read_uint())

