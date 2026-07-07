import re

from pathlib import Path

from gd_parser.crypto_data_buffer import CryptoDataBuffer
from gd_parser.gd_char_bio import GDCharBio


masteries = ["Soldier", "Demolitionist", "Occultist", "Nightblade", "Arcanist", "Shaman", "Inquisitor", "Necromancer", "Oathkeeper"]

classes = {
    # Classes puras
    "Soldier": "Soldier",
    "Demolitionist": "Demolitionist",
    "Occultist": "Occultist",
    "Nightblade": "Nightblade",
    "Arcanist": "Arcanist",
    "Shaman": "Shaman",
    "Inquisitor": "Inquisitor",
    "Necromancer": "Necromancer",
    "Oathkeeper": "Oathkeeper",

    # Soldier
    "Soldier + Demolitionist": "Commando",
    "Soldier + Occultist": "Witchblade",
    "Soldier + Nightblade": "Blademaster",
    "Soldier + Arcanist": "Battlemage",
    "Soldier + Shaman": "Warder",
    "Soldier + Inquisitor": "Tactician",
    "Soldier + Necromancer": "Death Knight",
    "Soldier + Oathkeeper": "Warlord",

    # Demolitionist
    "Demolitionist + Occultist": "Pyromancer",
    "Demolitionist + Nightblade": "Saboteur",
    "Demolitionist + Arcanist": "Sorcerer",
    "Demolitionist + Shaman": "Elementalist",
    "Demolitionist + Inquisitor": "Purifier",
    "Demolitionist + Necromancer": "Defiler",
    "Demolitionist + Oathkeeper": "Shieldbreaker",

    # Occultist
    "Occultist + Nightblade": "Witch Hunter",
    "Occultist + Arcanist": "Warlock",
    "Occultist + Shaman": "Conjurer",
    "Occultist + Inquisitor": "Deceiver",
    "Occultist + Necromancer": "Cabalist",
    "Occultist + Oathkeeper": "Sentinel",

    # Nightblade
    "Nightblade + Arcanist": "Spellbreaker",
    "Nightblade + Shaman": "Trickster",
    "Nightblade + Inquisitor": "Infiltrator",
    "Nightblade + Necromancer": "Reaper",
    "Nightblade + Oathkeeper": "Dervish",

    # Arcanist
    "Arcanist + Shaman": "Druid",
    "Arcanist + Inquisitor": "Mage Hunter",
    "Arcanist + Necromancer": "Spellbinder",
    "Arcanist + Oathkeeper": "Templar",

    # Shaman
    "Shaman + Inquisitor": "Vindicator",
    "Shaman + Necromancer": "Ritualist",
    "Shaman + Oathkeeper": "Archon",

    # Inquisitor
    "Inquisitor + Necromancer": "Apostate",
    "Inquisitor + Oathkeeper": "Paladin",

    # Necromancer
    "Necromancer + Oathkeeper": "Oppressor",
}

def get_class(cls):
    if pattern := re.fullmatch(r"\w+(\d{2})(\d{2})", cls):
        first_mastery = masteries[int(pattern[1]) - 1]
        second_mastery = masteries[int(pattern[2]) - 1]
        raw = f"{first_mastery} + {second_mastery}"
        return f"{raw}: {classes[raw]}"
    elif pattern := re.fullmatch(r"\w+(\d{2})", cls):
        mastery = masteries[int(pattern[1]) - 1]
        return mastery
    return None


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

        self.bio = GDCharBio(self.reader)

    # ----------------------------------------------------
    # Header
    # ----------------------------------------------------

    def read_header(self):

        self.name = self.reader.read_crypto_wstring()

        self.sex = self.reader.read_crypto_byte()

        raw_class = self.reader.read_crypto_string()
        self.char_class = get_class(raw_class)

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
        self.has_been_in_game = self.reader.read_crypto_bool()

        self.highest_difficulty = self.reader.read_crypto_byte()

        self.money = self.reader.read_crypto_uint()

        self.reader.read_block_end()


    def dump_next(self):
        print("NEXT BYTES:", self.reader.read_bytes(64))