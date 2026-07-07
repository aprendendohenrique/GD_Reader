class GDCharBio:
    def __init__(self, reader):
        self.reader = reader
        self.read()

    def read(self):
        version, length = self.reader.read_block_start()

        self.version = self.reader.read_crypto_int()

        self.level = self.reader.read_crypto_int()
        self.experience = self.reader.read_crypto_int()
        self.modifier_points = self.reader.read_crypto_int()
        self.skill_points = self.reader.read_crypto_int()
        self.devotion_points = self.reader.read_crypto_int()
        self.total_devotion = self.reader.read_crypto_int()

        self.total_strength = self.reader.read_crypto_float()
        self.total_agility = self.reader.read_crypto_float()
        self.total_intelligence = self.reader.read_crypto_float()
        self.health = self.reader.read_crypto_float()
        self.energy = self.reader.read_crypto_float()