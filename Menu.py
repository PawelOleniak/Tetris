import pygame
import sys
from Block import Block


pygame.init()
from ColorMods import BLACK, WHITE, GREY


class Button:
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(80, 30), font_name="Segoe Print", font_size=16, setvalue=-1):
        self.color = bg
        self.bg = bg
        self.fg = fg
        self.size = size
        self.changedsize = size
        self.shadowSize = [size[0] + 2.5, size[1] + 2.5]
        self.switched = False
        self.settedvalue = setvalue

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.center = [s // 2 for s in self.size]
        self.txt_surf = self.font.render(self.txt, True, self.fg)
        self.loc = [location[0]-self.center[0],location[1]-self.center[1]]
        self.txt_rect = self.txt_surf.get_rect(center=self.center)

        self.surface = pygame.surface.Surface(size)
        self.shadow = pygame.surface.Surface(self.shadowSize)
        self.rect = self.surface.get_rect(center=location)
        self.call_back_ = action


    def draw(self):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)

        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = (self.bg[0] * 0.8, self.bg[1] * 0.8, self.bg[2] * 0.8)

    def call_back(self):
        self.switched = not self.switched
        self.call_back_()


def mousebuttondown(buttons):
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            button.call_back()


def gradientRect(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)


screen = pygame.display.set_mode((400, 500))


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


menuBackground = Background("menu_background.png", [0, 0])


class menu:
    stop = False
    switched = False
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    width = 10
    height = 20
    colorindex = 0

    def changestate(self, state):
        self.state = state
        self.stop = True

    def changemode(self, state):
        self.state = state[int(self.switched)]
        self.stop = True

    def setwidth(self, width):
        self.width = width

    def setheight(self, height):
        self.height = height

    def changecolors(self, i):
        self.colorindex=i
        Block.colorindex=i

    def __init__(self):
        self.font = pygame.font.SysFont('Segoe Print', 20, True, False)
        self.tablelength = 9



        self.startButton = Button("Start", (200, 334), lambda: self.changestate("start"))
        self.loadButton = Button("Load", (200, 385), lambda: self.changestate("load"), bg=(0, 140, 80))
        self.hardButton = Button("Hard Mode", (200, 40), lambda: self.changemode(["hard", "normal"]), bg=(160, 40, 20), size=(120, 30))

        self.mixedcolors = Button("10", (50, 100), lambda: self.changecolors(2), bg=(16, 150, 20), size=(90, 25), setvalue=2)
        self.darkcolors = Button("10", (50, 50), lambda: self.changecolors(0), bg=(16, 150, 20), size=(90, 25), setvalue=0)
        self.lightcolors = Button("10", (50, 150), lambda: self.changecolors(1), bg=(16, 150, 20), size=(90, 25), setvalue=1)
        self.colorbuttons=[self.mixedcolors, self.darkcolors, self.lightcolors]

        self.ButtonW1 = Button("10", (160, 260), lambda: self.setwidth(10), bg=(16, 150, 20), size=(25, 15), setvalue=10)
        self.ButtonW2 = Button("14", (200, 260), lambda: self.setwidth(14), bg=(16, 150, 20), size=(25, 15), setvalue=14)
        self.ButtonW3 = Button("18", (240, 260), lambda: self.setwidth(18), bg=(16, 150, 20), size=(25, 15), setvalue=18)
        self.Wbuttons = [self.ButtonW1, self.ButtonW2, self.ButtonW3]

        self.ButtonH1 = Button("20", (280, 100), lambda: self.setheight(20), bg=(16, 150, 20), size=(25, 15), setvalue=20)
        self.ButtonH2 = Button("24", (280, 150), lambda: self.setheight(24), bg=(16, 150, 20), size=(25, 15), setvalue=24)
        self.ButtonH3 = Button("28", (280, 200), lambda: self.setheight(28), bg=(16, 150, 20), size=(25, 15), setvalue=28)
        self.Hbuttons = [self.ButtonH1, self.ButtonH2, self.ButtonH3]

        self.buttons = [self.startButton, self.loadButton, self.hardButton, self.ButtonW1, self.ButtonW2, self.ButtonW3,
                        self.ButtonH1, self.ButtonH2, self.ButtonH3,
                        self.mixedcolors, self.darkcolors, self.lightcolors,
                        ]

    def Open(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousebuttondown(self.buttons)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.changestate("start")
            screen.blit(menuBackground.image, menuBackground.rect)
            sizechange = [self.height - 20, self.width - 10]
            pygame.draw.rect(screen, (50 + int(self.switched) * 200, 50, 150 - int(self.switched) * 150),
                             pygame.Rect(160-sizechange[1]*2, 95-sizechange[0]*2, 80 + sizechange[1]*4, 130 + sizechange[0]*4))
            for button in self.buttons:
                if button.settedvalue == self.width or button.settedvalue == self.height or button.settedvalue == self.colorindex:
                    pygame.draw.rect(screen, (250, 100, 100), pygame.Rect(button.loc[0]-1, button.loc[1]-1, button.shadowSize[0], button.shadowSize[1]))
                button.draw()

            gradientRect(screen, (100, 200, 100), (180, 20, 122), pygame.Rect(5, 88, 90, 25))
            gradientRect(screen, (120, 37, 179), (180, 34, 122), pygame.Rect(5, 38, 90, 25))
            gradientRect(screen, (100, 200, 100), (200, 150, 120), pygame.Rect(5, 138, 90, 25))
            with open("ranking.txt", "a+") as data:
                text = self.font.render("Ranking:", True, GREY)
                screen.blit(text, [260, 55])
                data.seek(0, 0)
                lines = data.readlines()
                if len(lines)<9:
                    self.tablelength=len(lines)
                for i in range(self.tablelength):
                    text = self.font.render(str(i+1)+". "+str(int(lines[i])), True, (250-20*i,220-20*i,20))
                    screen.blit(text, [310, 80+20*i])


            pygame.display.flip()
            pygame.time.wait(40)
            if self.stop:
                break
