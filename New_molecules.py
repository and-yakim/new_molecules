from tkinter import *
from random import uniform
import quadtree


class Molecule:
    def __init__(self, x, y, canvas):
        self.x,  self.y = x, y
        self.canvas = canvas
        self.id = self.draw()

    def draw(self):
        radius = 10
        return self.canvas.create_oval(self.x - radius, self.y - radius,
                                       self.x + radius, self.y + radius,
                                       fill='brown', width=1)

    def move(self, dx, dy):
        self.canvas.coords(self.id, dx, dy)


class MoleculesSimulator:
    def __init__(self):
        self.width, self.height = 800, 500
        self.root = Tk()
        self.root.geometry('+300+100')

        self.field = Canvas(self.root, width=self.width,
                            height=self.height, bg='silver')
        self.field.pack()

        self.gas: [Molecule] = []
        for i in range(100):
            self.gas.append(Molecule(uniform(0, self.width),
                                     uniform(0, self.height), self.field))

        self.root.mainloop()


def main():
    MoleculesSimulator()


if __name__ == '__main__':
    main()
