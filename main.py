from pathlib import Path

from gd_parser.character_reader import CharacterReader


def main():
    path = Path(r"C:\Program Files (x86)\Steam\userdata\913021940\219990\remote\save\main\_Roda Qualitativa/player.gdc")
    character = CharacterReader(path)

    print(character.name)
    print(character.level)
    # print(character.char_class)

    print(character.bio.mastery_1)
    print(character.bio.mastery_2)
    # print(character.hardcore)
    # print(character.money)
    # print(character.highest_difficulty)

if __name__ == "__main__":
    main()