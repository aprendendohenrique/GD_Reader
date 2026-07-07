import sys
from time import sleep

from pypresence import Presence


class Discord:

    def __init__(self):
        self.CLIENT_ID = "1524024904368914503"

        self.rpc = Presence(self.CLIENT_ID)
        self.rpc.connect()

    def update(self):
        while True:
            self.rpc.update(
                details=f"👤 {self.name}",
                state=f"⚔️ {self.cls}\n • Lv.{self.level}",
            )

            try:
                input("Press Enter to Close Program")
                break
            except KeyboardInterrupt:
                sys.exit("--Program Closed--")

    def update_info(self, name, level, cls):
        self.name = name
        self.level = level
        self.cls = cls