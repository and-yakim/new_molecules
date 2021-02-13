class Quadrant:
    table = [[j.split(',') for j in i.split()] for i in open('table.txt')]
    MAX_DEPTH = 5

    def __init__(self, dots, particles, level, num, address):
        self.dots = dots
        self.particles = particles
        self.level = level
        self.num = num
        self.address = address
        self.nested_quads = self.divide()

    def divide(self):
        if not len(self.particles) or self.level == self.MAX_DEPTH:
            return []
        else:
            return []
