from Block import Block


class Tetris:

    field = []
    x = 100
    y = 60
    zoom = 20
    figure = None

    def __init__(self, height, width, speed=2, middle=3):

        self.scored = False
        self.height = height
        self.width = width
        self.field = []
        self.level = speed
        self.score = 0
        self.gameState = "start"
        self.middle = middle
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def load(self):
        odplist = []
        content = []
        with open("save.txt", 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                content.append(currentPlace)
        with open("saveddata.txt", 'r')as f:
            s = f.readline()
            x = f.readline()
            y = f.readline()
        i = 0
        for el in content:
            content[i]=el
            odp = [int(s) for s in content[i]]
            odplist.append(odp)
            i=i+1

        return int(y), int(x), int(s), odplist

    def new_block(self):
        self.figure = Block(self.middle, 0)

    def change_Gamestate(self, state):
        self.gameState = state

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0          or self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def deleteline(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
#pokaz nowy blok
    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()
#zatrzymaj
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.deleteline()
        self.new_block()
        if self.intersects():
            self.gameState = "gameover"
#przesuń
    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


