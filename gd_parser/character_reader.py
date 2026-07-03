from pathlib import Path

from gd_parser.crypto_data_buffer import CryptoDataBuffer
from gd_parser.gd_char_bio import GDCharBio


CLASS_NAMES = {
        "tagSkillClassName0001": "Soldier",
        "tagSkillClassName0002": "Demolitionist",
        "tagSkillClassName0003": "Occultist",
        "tagSkillClassName0004": "Nightblade",
        "tagSkillClassName0005": "Arcanist",
        "tagSkillClassName0006": "Shaman",
        "tagSkillClassName0508": "Oathkeeper",
        "tagSkillClassName0509": "Necromancer",
    }

def translate_class(tag: str) -> str:
    return CLASS_NAMES.get(tag, tag)


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

        zero = self.reader.read_crypto_int(update_key=False)

        version = self.reader.read_crypto_int()

        self.reader.read_and_discard_uid()

        self.read_character_info()
        while True:
            try:
                val = self.reader.read_crypto_string()
                print("STRING FOUND:", val)
                break
            except:
                self.reader.cursor += 1

        self.reader.read_block_start()

        print("=== DEBUG BEFORE BIO ===")
        self.reader.debug_stream(5)

        self.bio = GDCharBio(self.reader)

    # ----------------------------------------------------
    # Header
    # ----------------------------------------------------

    def read_header(self):

        self.name = self.reader.read_crypto_wstring()

        self.sex = self.reader.read_crypto_byte()

        raw_class = self.reader.read_crypto_string()
        self.char_class = translate_class(raw_class)

        self.level = self.reader.read_crypto_int()

        self.hardcore = self.reader.read_crypto_bool()

        self.reader.read_block_end()

    # ----------------------------------------------------
    # Character info
    # ----------------------------------------------------

    def read_character_info(self):
        self.reader.read_block_start()

        version = self.reader.read_crypto_int()

        self.is_in_main_quest = self.reader.read_crypto_bool()

    def dump_next(self):
        print("NEXT BYTES:", self.reader.read_bytes(64))