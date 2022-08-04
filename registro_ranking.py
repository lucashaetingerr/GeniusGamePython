class RegistroRanking:
    def __init__(self):
        self.nome = ''
        self.score = 0

    def to_string(self):
        return '{};{}'.format(self.nome, self.score)

    def from_string(self, string: str):
        split = string.replace('\n', '').split(';', 2)
        self.nome = split[0]
        self.score = int(split[1])
