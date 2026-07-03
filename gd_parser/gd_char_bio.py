class GDCharBio:

    def __init__(self, reader):
        self.reader = reader

        self.mastery_1 = None
        self.mastery_2 = None

        self.read()

    def read(self):
        # entra no bloco do Bio
        self.reader.read_block_start()

        # ⚠️ aqui começa o que nos interessa

        # Mastery 1
        self.mastery_1 = self.reader.read_crypto_string()

        # Mastery 2
        self.mastery_2 = self.reader.read_crypto_string()

        # sai do bloco
        self.reader.read_block_end()