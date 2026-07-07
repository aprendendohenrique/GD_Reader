import sys

import sys
from pathlib import Path

from gd_parser.character_reader import CharacterReader
from discord import Discord


def main():
    path = Path(r"C:\Program Files (x86)\Steam\userdata\913021940\219990\remote\save\main")

    file_names = []
    for count, file in enumerate(path.iterdir()):
        name = file.name.replace("_", "")

        print(f"{count+1} - {name}")
        file_names.append(file.name)

    try:
        player_choice = int(input("Choice: "))
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()

    path = path / file_names[player_choice-1] / "player.gdc"

    character = CharacterReader(path)

    # print(character.name)
    # print(character.level)
    # print(character.char_class)

    # Discord
    discord = Discord()
    discord.update_info(character.name, f"{character.level}", character.char_class)
    discord.update()

if __name__ == "__main__":
    main()