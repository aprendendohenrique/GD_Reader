from pathlib import Path


def main():
    path = Path(r"C:\Program Files (x86)\Steam\userdata\913021940\219990\remote\save\main")
    characters = []

    print("Characters: ")
    for count, file in enumerate(path.iterdir()):
        characters.append(file)
        print(f"{count+1} - {file.name.replace('_', '')}")

    choice = int(input("Choice: ").strip())
    char_path = Path(f"{characters[choice - 1]}\player.gdc")
    with open(char_path, "rb") as file:
        print(file.readlines())


if __name__ == '__main__':
    main()

