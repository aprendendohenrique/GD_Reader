from pathlib import Path

from gd_parser.crypto_data_buffer import CryptoDataBuffer


class CharacterReader:

    def __init__(self, file_path):
        self.file_path = Path(file_path)

        with open(self.file_path, "rb") as file:
            data = file.read()

        self.reader = CryptoDataBuffer(data)

        # Character info
        self.name = ""
        self.level = 0
        self.char_class = ""

        self.sex = 0
        self.hardcore = False

        self.is_in_main_quest = False
        self.has_been_in_game = False

        self.highest_difficulty = 0
        self.money = 0

        self.read_summary()

    # ----------------------------------------------------
    # Main reader
    # ----------------------------------------------------

    def read_summary(self):

        self.reader.read_crypto_key()

        magic = self.reader.read_crypto_int()

        if magic != 0x58434447:
            raise ValueError("Invalid Grim Dawn save.")

        save_version = self.reader.read_crypto_int()

        self.read_header()
        print(hex(self.reader.cursor))

        zero = self.reader.read_crypto_int(update_key=False)

        version = self.reader.read_crypto_int()

        self.reader.read_and_discard_uid()
        print(hex(self.reader.cursor))

        self.read_character_info()

        # Bio será implementado depois
        # self.bio = GDBio(self.reader)

    # ----------------------------------------------------
    # Header
    # ----------------------------------------------------

    def read_header(self):

        self.name = self.reader.read_crypto_wstring()

        self.sex = self.reader.read_crypto_byte()

        self.char_class = self.reader.read_crypto_string()

        self.level = self.reader.read_crypto_int()

        self.hardcore = self.reader.read_crypto_bool()

        self.reader.read_block_end()

    # ----------------------------------------------------
    # Character info
    # ----------------------------------------------------

    def read_character_info(self):
        print(hex(self.reader.cursor))

        self.reader.read_block_start()

        print(hex(self.reader.cursor))

        version = self.reader.read_crypto_int()

        print(hex(self.reader.cursor))

        self.is_in_main_quest = self.reader.read_crypto_bool()

        print(hex(self.reader.cursor))