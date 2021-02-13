from tkinter import *
from random import uniform


window_x, window_y = 400, 0
width, height = 1000, 1000
radius = 2
n = 1000
max_depth = 6


class Molecule:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def draw_particle(self):
        field.create_oval(self.x - radius, self.y - radius, self.x + radius, self.y + radius,
                          fill='brown', width=1)


class QuadTree:
    table = [[j.split(',') for j in i.split()] for i in open('table.txt')]
    sub_table = [i[0] for i in table]

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
        self.draw_borders()

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
        return output

    def search_by_address(self, address):
        temp = self.root_node
        while temp.root_node is not None:
            temp = temp.root_node
        for i in address:
            flag = False
            for j in temp.nested_quadrants:
                if j.num == i:
                    temp = j
                    flag = True
                    break
            if not flag:
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
        neighbors = self.sub_table
        for i in range(len(neighbors)):
            neighbors[i] = self.search(neighbors[i])
        return neighbors

    def destruct(self):
        for i in range(len(self.root_node.nested_quadrants)):
            if self.root_node.nested_quadrants[i].num == self.num:
                self.root_node.nested_quadrants.pop(i)
                break

    def draw_borders(self):
        field.create_rectangle(self.x_left, self.y_top, self.x_right, self.y_bot,
                               width=1, outline='blue')


root = Tk()
root.geometry(str(width) + 'x' + str(height) + '+' + str(window_x) + '+' + str(window_y))
field = Canvas(root, width=width, height=height, bg='silver')
field.pack()
gas = [Molecule(uniform(0, width), uniform(0, height)) for i in range(n)]
tree = QuadTree(particles=gas, x_right=width, y_bot=height)
for i in gas:
    i.draw_particle()
root.mainloop()
