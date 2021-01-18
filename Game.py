import pygame

import Menu
import time
from ColorMods import Colors, WHITE, GREY
from main import Tetris


class again(Exception):
    pass


pygame.init()


pygame.display.set_caption("Tetris")
font = pygame.font.SysFont('Calibri', 30, True, False)

text_game_over = font.render("Game Over", True, (255, 255, 250))
text_game_over1 = font.render("Enter- new game", True, (0, 0, 0))
text_game_over2 = font.render("Esc- exit", True, (0, 0, 0))

MainState = "menu"


speed = 2
clock = pygame.time.Clock()
fps = 25
counter = 0

pressing_down = False

while True:
    while MainState == "menu":
        Menu1 = Menu.menu()
        Menu1.Open()
        MainState = Menu1.state

    if MainState == "hard":
        speed += 4
        MainState = "menu"
        Menu.menu.switched = True
        continue
    if MainState == "normal":
        speed -= 4
        MainState = "menu"
        Menu.menu.switched = False
        continue


    size = (Menu1.width * 20 + 200, Menu1.height * 20 + 100)
    gamesize = (Menu1.width * 20, Menu1.height * 20)
    game = Tetris(Menu1.height, Menu1.width, speed, Menu1.width // 2 - 2)
    screen = pygame.display.set_mode(size)



    if MainState == "load":
        x,y,s,z=game.load()
        size = (x * 20 + 200, y * 20 + 100)
        gamesize = (x* 20, y * 20)
        game1 = Tetris(y, x, speed, x // 2 - 2)
        game1.field=z
        screen = pygame.display.set_mode(size)
        MainState = "start"
        game1.score=s

        game = game1
    if speed==2:
        gameBackground = Menu.Background("game_background_main.jpg", [0, -660 + size[1]])
    else:
        gameBackground = Menu.Background("game_background_Dark.jpg", [0, -660 + size[1]])

    try:
        while MainState == "start":

            if game.figure is None:
                game.new_block()
            counter += 1
            if counter > 100000:
                counter = 0

            if counter % (fps // game.level // 2) == 0 or pressing_down:
                if game.gameState == "start":
                    game.go_down()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    t = time.time() + 5
                    if not game.gameState=="gameover":

                        while time.time() < t:
                                g=pygame.event.poll()
                                pygame.draw.rect(screen, WHITE, [10, 190, 220, 50])
                                textsave = font.render("Save?(Enter) " + str(int((t - time.time()) % 10)), True, (255, 125, 0))
                                screen.blit(text_game_over2, [1, size[1]-85])
                                screen.blit(textsave, [20, 200])
                                if g.type == pygame.KEYDOWN and g.key == pygame.K_RETURN:
                                    with open("saveddata.txt","w") as data:
                                        data.write(str(game.score)+"\n"+str(Menu1.height)+"\n"+str(Menu1.width))

                                    with open("save.txt", "w") as lastsave:
                                        for listitem in game.field:
                                            for cube in listitem:
                                                lastsave.write('%d' % int(cube))
                                            lastsave.write("\n")
                                    screen = pygame.display.set_mode((400, 500))
                                    raise again

                                elif g.type == pygame.KEYDOWN and g.key == pygame.K_ESCAPE:
                                    screen = pygame.display.set_mode((400, 500))
                                    raise again

                                pygame.display.flip()
                        screen = pygame.display.set_mode((400, 500))
                    screen = pygame.display.set_mode((400, 500))
                    raise again

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_RETURN:
                        game.__init__(Menu1.height, Menu1.width, speed, Menu1.width // 2 - 2)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        pressing_down = False

            screen.blit(gameBackground.image, gameBackground.rect)
            pygame.draw.rect(screen, WHITE, [100, 60, gamesize[0], gamesize[1]])

            for i in range(game.height):
                for j in range(game.width):
                    pygame.draw.rect(screen, GREY,
                                     [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                     1)
                    if game.field[i][j] > 0:
                        pygame.draw.rect(screen, Colors[Menu1.colorindex][game.field[i][j]],
                                         [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                          game.zoom - 1])

            if game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in game.figure.image():
                            pygame.draw.rect(screen,
                                                Colors[Menu1.colorindex]
                             [game.figure.color],
                                             [game.x + game.zoom * (j + game.figure.x) + 1,
                                              game.y + game.zoom * (i + game.figure.y) + 1,
                                              game.zoom - 2, game.zoom - 2])

            text = font.render("Score: " + str(game.score), True, WHITE)
            screen.blit(text, [0, 0])
            if game.gameState == "gameover":
                screen.blit(text_game_over, [120, 20])
                screen.blit(text_game_over1, [2, size[1]-35])
                screen.blit(text_game_over2, [1, size[1]-85])
                if not game.scored:
                    with open("ranking.txt", "a+") as data:
                        data.seek(0, 0)
                        lines = data.readlines()
                        for i in range(len(lines)):
                            lines[i] = int(lines[i])
                        lines.append(game.score)
                        lines.sort(reverse=True)
                        print(lines)
                        data.truncate(0)
                        for i in range(len(lines)):
                            data.write(str(lines[i]) + "\n")
                    game.scored = True

            pygame.display.flip()
            clock.tick(fps)
    except again:
        MainState = "menu"
