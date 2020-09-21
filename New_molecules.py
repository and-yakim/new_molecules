from tkinter import *


class Quadrant:
    def __init__(self):
        pass


class Molecules:
    def __init__(self):
        pass


class MoleculesSimulator:
    def __init__(self):
        self.width, self.height = 800, 500
        self.root = Tk()
        self.root.geometry('+300+100')

        self.field = Canvas(self.root, width=self.width,
                            height=self.height, bg='silver')
        self.field.pack()

        self.root.mainloop()


def main():
    MoleculesSimulator()


if __name__ == '__main__':
    main()
