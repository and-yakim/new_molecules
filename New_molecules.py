from tkinter import *
from random import uniform
from time import time
from math import *
import matplotlib.pyplot as plt


class Molecule:
    def __init__(self, x, y, v_x, v_y, iden):
        self.x, self.y = x, y
        self.old_x, self.old_y = x, y
        self.v_x, self.v_y = v_x, v_y
        self.iden = iden

    def move(self):
        self.x += self.v_x
        self.y += self.v_y

    def draw_particle(self, field):
        field.move(self.iden, self.x - self.old_x, self.y - self.old_y)
        self.old_x, self.old_y = self.x, self.y

    def border_check(self):
        if self.x < rc:
            self.v_x += coef * (radius2 / (2 * self.x) ** 2) ** 7 * (2 * self.x)
        elif self.x > width - rc:
            self.v_x += - coef * (radius2 / (2 * (width - self.x)) ** 2) ** 7 * (2 * (width - self.x))
        if self.y < rc:
            self.v_y += coef * (radius2 / (2 * self.y) ** 2) ** 7 * (2 * self.y)
        elif self.y > height - rc:
            self.v_y += - coef * (radius2 / (2 * (height - self.y)) ** 2) ** 7 * (2 * (height - self.y))


def force(mol1, mol2):
    r2 = (mol1.x - mol2.x) ** 2 + (mol1.y - mol2.y) ** 2
    if r2 < rc2:
        f1 = radius2 / r2
        f2 = f1 ** 3
        df = - coef * (- f2 ** 2 * f1 + f2 * f1) - fc
        mol1.v_x += df * (mol2.x - mol1.x)
        mol1.v_y += df * (mol2.y - mol1.y)
        mol2.v_x += df * (mol1.x - mol2.x)
        mol2.v_y += df * (mol1.y - mol2.y)
        potentialEnergy[-1] += 2 * coef * radius2 / 12 * (f2 ** 2 - f2) - uc
        kineticEnergy[-1] += (mol1.v_x ** 2 + mol1.v_x ** 2 + mol2.v_x ** 2 + mol2.v_y ** 2) / 2


def check(gas):
    potentialEnergy.append(0)
    kineticEnergy.append(0)
    for i in range(len(gas) - 1):
        for j in range(i + 1, len(gas)):
            if abs(gas[i].x - gas[j].x) < 2.5 * rc and \
                    abs(gas[i].y - gas[j].y) < 2.5 * rc:
                force(gas[i], gas[j])


def redraw(field, gas, period):
    global frame
    if fps > 60:
        period = fps // 60
    if frame >= period:
        for i in gas:
            i.draw_particle(field)
        frame = 1
    else:
        frame += 1


def render(root, gas, field):
    if flag:
        check(gas)
        for i in gas:
            i.move()
            i.border_check()
        redraw(field, gas, 1)
        fps_title(root)
        root.after(1, lambda: render(root, gas, field))


def initialization(field):
    gas = []
    diameter = 2 * radius
    for i in range(width // diameter):
        for j in range(height // diameter):
            fi = uniform(0, 2 * pi)
            v = uniform(velocity / 2, velocity)
            v_x = v * cos(fi)
            v_y = v * sin(fi)
            gas.append(Molecule(radius + diameter * i,
                                radius + diameter * j, v_x, v_y,
                                field.create_oval(diameter * i, diameter * j,
                                                  diameter * (i + 1), diameter * (j + 1),
                                                  fill='brown', width=1)))
    return gas


def fps_title(root):
    global t, fps
    temp = time()
    fps = int(1 / (temp - t))
    root.title("FPS = " + str(fps))
    t = temp


def pause(root, gas, field):
    global flag
    flag = False if flag else True
    if not flag:
        root.title("...Pause...")
        temp = [i for i in range(1, len(potentialEnergy) + 1)]
        plt.plot(temp, potentialEnergy, 'b', markersize=2)
        plt.plot(temp, kineticEnergy, 'r', markersize=2)
        plt.plot(temp, [kineticEnergy[i] + potentialEnergy[i] for i in range(len(temp))],
                 'g', markersize=2)
        plt.show()
    root.after(1, render(root, gas, field))


def keypress(button, root, field):
    global width, height
    if button == 'a':
        width *= 0.9995
    elif button == 'w':
        height *= 0.9995
    elif button == 'd':
        width *= 1.0005
    elif button == 's':
        height *= 1.0005
    root.geometry(str(round(width)) + 'x' + str(round(height)) +
                  '+' + str(window_x) + '+' + str(window_y))
    field.config(width=width, height=height)


def keypress2(button, gas):
    if button == 'q':
        for i in gas:
            i.v_x *= 0.95
            i.v_y *= 0.95
    elif button == 'e':
        for i in gas:
            i.v_x *= 1.05
            i.v_y *= 1.05


window_x, window_y = 300, 0
width, height = 1000, 1000
radius = 4
radius2 = radius ** 2
rc = radius * 2.5
rc2 = rc ** 2
coef = 1
fc = - coef * (- 1 / 2.5 ** 14 + 1 / 2.5 ** 8)
uc = 2 * coef * radius2 / 12 * (1 / 2.5 ** 12 - 1 / 2.5 ** 6)
velocity = radius / 100
flag = True
t = time()
fps = 0
frame = 1
kineticEnergy = []
potentialEnergy = []


def main():
    root = Tk()
    root.geometry(str(width) + 'x' + str(height) +
                  '+' + str(window_x) + '+' + str(window_y))
    field = Canvas(root, width=width, height=height, bg='silver')
    field.pack()
    gas = initialization(field)
    print("n = " + str(len(gas)))
    render(root, gas, field)
    root.bind('<space>', lambda event: pause(root, gas, field))
    root.bind('<KeyPress-a>', lambda event: keypress('a', root, field))
    root.bind('<KeyPress-w>', lambda event: keypress('w', root, field))
    root.bind('<KeyPress-d>', lambda event: keypress('d', root, field))
    root.bind('<KeyPress-s>', lambda event: keypress('s', root, field))
    root.bind('<KeyPress-q>', lambda event: keypress2('q', gas))
    root.bind('<KeyPress-e>', lambda event: keypress2('e', gas))
    root.mainloop()


if __name__ == '__main__':
    main()
