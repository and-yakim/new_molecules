from tkinter import *
import random
from time import time
import math
import matplotlib.pyplot as plt


window_x, window_y = 300, 0
width, height = 1000, 1000
radius = 20
radius2 = radius ** 2
rc = math.log(2 ** (1 / 6) * radius)
rc2 = rc ** 2
dt = 0.1
max_depth = math.floor(- math.log(rc / min(width, height)) / math.log(2))


class Molecule:
    def __init__(self, x, y, v_x, v_y, iden):
        self.x, self.y = x, y
        self.old_x, self.old_y = x, y
        self.v_x, self.v_y = v_x, v_y
        self.iden = iden

    def move(self):
        self.x = (self.x + self.v_x * dt + width) % width
        self.y = (self.y + self.v_y * dt + height) % height

    def draw_particle(self, field):
        field.move(self.iden, self.x - self.old_x, self.y - self.old_y)
        self.old_x, self.old_y = self.x, self.y


class QuadTree:
    table = [[j.split(',') for j in i.split()] for i in open('table.txt')]
    sub_table = [i[0] for i in table]
    deep_quadrants = []

    def __init__(self, particles=[], root_node=None, level=0, num=0, address='',
                 x_left=0, y_top=0, x_right=width, y_bot=height):
        self.root_node = root_node
        self.particles = particles
        self.level = level
        self.num = num
        self.address = address
        self.x_left, self.y_top = x_left, y_top
        self.x_right, self.y_bot = x_right, y_bot
        self.nested_quadrants = self.divide() if len(self.particles) > 0 and self.level < max_depth else []
        if self.level == max_depth:
            self.deep_quadrants.append(self)

    def create_quadrant(self, particles, num):
        w = (self.x_right - self.x_left) / 2
        h = (self.y_bot - self.y_top) / 2
        x_left = self.x_left + w * (num % 2)
        y_top = self.y_top + h * (int(num / 2) % 2)
        x_right = self.x_right - w * ((num + 1) % 2)
        y_bot = self.y_bot - h * (int(num / 2 + 1) % 2)
        return QuadTree(particles, self, self.level + 1, num, self.address + str(num),
                        x_left, y_top, x_right, y_bot)

    def place(self, particle):
        if particle.x < (self.x_left + self.x_right) / 2:
            num = 0
        else:
            num = 1
        if particle.y > (self.y_top + self.y_bot) / 2:
            num += 2
        return num

    def divide(self):
        temp = [[] for i in range(4)]
        for i in self.particles:
            temp[self.place(i)].append(i)
        output = [None, None, None, None]
        for i in range(len(temp)):
            if len(temp[i]) > 0:
                output[i] = (self.create_quadrant(temp[i], i))
        while output.count(None) > 0:
            output.remove(None)
        return output

    def search_by_address(self, address):
        temp = self.root_node
        while temp.root_node is not None:
            temp = temp.root_node
        for i in address:
            flag_temp = False
            for j in temp.nested_quadrants:
                if j.num == i:
                    temp = j
                    flag_temp = True
                    break
            if not flag_temp:
                return None
        return temp

    def search(self, direction):
        address = ''
        for i in self.address[-1]:
            temp, direction = self.table[self.sub_table.index(direction)][int(i) + 1]
            address = temp + address
            if direction == 'stop':
                address = self.address[:self.level + 1 - len(address)] + address
                break
        return self.search_by_address(address)

    def neighborhood(self):
        neighbors = []
        for i in range(len(self.sub_table)):
            temp = self.search(self.sub_table[i])
            if temp is not None:
                neighbors.append(temp)
        return neighbors

    def destruct(self):
        for i in range(len(self.root_node.nested_quadrants)):
            if self.root_node.nested_quadrants[i].num == self.num:
                for k in range(len(self.particles)):
                    for p in range(len(self.root_node.particles)):
                        if self.particles[k] == self.root_node.particles[p]:
                            self.root_node.particles.pop(p)
                            break
                self.root_node.nested_quadrants.pop(i)
                break


def force(mol1, mol2):
    rx = mol2.x - mol1.x
    ry = mol2.y - mol1.y
    r2 = rx ** 2 + ry ** 2
    if r2 < rc2:
        f2 = 1 / r2  # f = r ** (- 1)
        f6 = f2 ** 3
        temp = 48 * (f6 ** 2 * f2 - 0.5 * f6 * f2) * dt
        mol1.v_x += temp * rx
        mol1.v_y += temp * ry
        mol2.v_x -= temp * rx
        mol2.v_y -= temp * ry
        potentialEnergy[-1] += 4 * (f6 ** 2 - f6)
    elif r2 > 2 * rc:
        rx = (rx + width) % width
        ry = (ry + height) % height
        f2 = 1 / r2
        f6 = f2 ** 3
        temp = 48 * (f6 ** 2 * f2 - 0.5 * f6 * f2) * dt
        mol1.v_x += temp * rx
        mol1.v_y += temp * ry
        mol2.v_x -= temp * rx
        mol2.v_y -= temp * ry
        potentialEnergy[-1] += 4 * (f6 ** 2 - f6)
    # print('F')


def check(gas):
    potentialEnergy.append(0)
    kineticEnergy.append(0)
    QuadTree.deep_quadrants = []
    tree = QuadTree(gas)
    print(len(QuadTree.deep_quadrants))
    for i in QuadTree.deep_quadrants:
        if len(i.particles) > 1:
            for p in range(len(i.particles) - 1):
                for k in range(p + 1, len(i.particles)):
                    force(i.particles[p], i.particles[k])
        for j in i.neighborhood():
            for p in range(len(i.particles)):
                for k in range(len(j.particles)):
                    force(i.particles[p], j.particles[k])
        i.destruct()
    for i in gas:
        kineticEnergy[-1] += 0.5 * (i.v_x ** 2 + i.v_y ** 2)


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
        # check(gas)
        for i in gas:
            i.move()
        redraw(field, gas, 1)
        fps_title(root)
        root.after(1, lambda: render(root, gas, field))


def initialization(field):
    gas = []
    diameter = 2 * radius
    for i in range(width // diameter):
        for j in range(height // diameter):
            fi = random.uniform(0, 2 * math.pi)
            v = random.uniform(velocity / 2, velocity)
            v_x = v * math.cos(fi)
            v_y = v * math.sin(fi)
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


velocity = radius / 10
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
