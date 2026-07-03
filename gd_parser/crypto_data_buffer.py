import struct

from gd_parser.data_buffer import DataBuffer


class CryptoDataBuffer(DataBuffer):
    XOR_KEY = 1431655765
    PRIME = 39916801

    def __init__(self, data: bytes):
        super().__init__(data)

        self.key = 0
        self.table = [0] * 256

    # -------------------------
    # Internal methods
    # -------------------------

    @staticmethod
    def rotate_right(value: int) -> int:
        return ((value >> 1) | (value << 31)) & 0xFFFFFFFF

    def generate_table(self, key: int):
        self.table = [0] * 256

        for i in range(256):
            key = self.rotate_right(key)
            key = (key * self.PRIME) & 0xFFFFFFFF
            self.table[i] = key

    def update_key(self, raw: bytes):
        for byte in raw:
            self.key ^= self.table[byte]

    def _decrypt_uint(self) -> int:
        raw = self.read_uint()

        value = raw ^ self.key

        self.update_key(struct.pack("<I", raw))

        return value & 0xFFFFFFFF

    def _decrypt_byte(self, raw: int) -> int:
        value = raw ^ (self.key & 0xFF)

        self.key ^= self.table[raw]

        return value & 0xFF

    def _decrypt_bytes(self, amount: int) -> bytes:
        raw = self.read_bytes(amount)

        result = bytearray()

        for byte in raw:
            result.append(self._decrypt_byte(byte))

        return bytes(result)

    # -------------------------
    # Public methods
    # -------------------------

    def read_crypto_key(self):
        raw = self.read_uint()

        self.key = raw ^ self.XOR_KEY

        self.generate_table(self.key)

    def _read_crypto_uint_raw(self, update_key=True):
        raw = self.read_uint()

        value = raw ^ self.key

        if update_key:
            self.update_key(struct.pack("<I", raw))

        return value & 0xFFFFFFFF

    def read_crypto_uint(self, update_key=True):
        return self._read_crypto_uint_raw(update_key)

    def read_crypto_int(self, update_key=True):
        value = self._read_crypto_uint_raw(update_key)
        return struct.unpack("<i", struct.pack("<I", value))[0]

    def read_crypto_float(self):
        value = self._decrypt_uint()

        return struct.unpack("<f", struct.pack("<I", value))[0]

    def read_crypto_byte(self):
        raw = self.read_byte()

        return self._decrypt_byte(raw)

    def read_crypto_bool(self):
        return self.read_crypto_byte() == 1

    def read_crypto_string(self):
        length = self.read_crypto_uint()

        if length == 0:
            return ""

        return self._decrypt_bytes(length).decode("ascii")

    def read_crypto_wstring(self):
        length = self.read_crypto_uint()

        if length == 0:
            return ""

        return self._decrypt_bytes(length * 2).decode("utf-16-le")

    def read_and_discard_uid(self):
        for _ in range(16):
            self.read_crypto_byte()

    def read_block_start(self):
        block_version = self.read_crypto_int()
        block_length = self.read_crypto_int(False)

        return block_version, block_length

    def read_block_end(self):
        return self.read_crypto_int() == 0