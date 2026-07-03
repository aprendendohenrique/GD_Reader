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
        self.generate_table(self.key)

    def generate_table(self, key):
        self.table = [0] * 256

        for i in range(256):
            key = self.rotate_right(key)
            key *= 39916801
            key &= 0xFFFFFFFF
            self.table[i] = key

    def rotate_right(self, value):
        return ((value >> 1) | (value << 31)) & 0xFFFFFFFF

    def update_key(self, byts):
        for byte in byts:
            self.key ^= self.table[byte]

    def read_crypto_uint(self, byte):
        raw = self.read_uint()

        value = raw ^ self.key

        self.update_key(struct.pack("<I", raw))

        return value



data = struct.pack("<I", 1000)
buffer = DataBuffer(data)
buffer.read_crypto_key()

