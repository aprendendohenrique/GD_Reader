class GDCharBio:

    def __init__(self, reader):
        self.reader = reader

        self.mastery_1 = None
        self.mastery_2 = None

        self.read()

    def read(self):
        print("BIO cursor start:", hex(self.reader.cursor))

        # version, length = self.reader.read_block_start()
        print(hex(self.reader.cursor))

        for i in range(10):
            print(i, self.reader.read_crypto_uint(False))

        # print("BIO version:", version)
        # print("BIO length:", length)
        print("Cursor after block start:", hex(self.reader.cursor))

        length = self.reader.read_crypto_uint()
        print("First uint (string length?):", length)

        raise SystemExit