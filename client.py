import pygame
from network import Network
from Button import Button
import pickle

pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
<<<<<<< HEAD
bg = pygame.image.load("assets/menuScreen3.jpg")
bg = pygame.transform.scale(bg, (width, height))
bg_loading = pygame.transform.scale(pygame.image.load("assets/waitScreen.gif"), (width, height))


# class Button:
#     def __init__(self, text, x, y, color):
#         self.text = text
#         self.x = x
#         self.y = y
#         self.color = color
#         self.width = 150
#         self.height = 100
#
#     def draw(self, win):
#         pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
#         font = pygame.font.SysFont("comicsans", 40)
#         text = font.render(self.text, 1, (255, 255, 255))
#         win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
#                         self.y + round(self.height / 2) - round(text.get_height() / 2)))
#
#     def click(self, pos):
#         x1 = pos[0]
#         y1 = pos[1]
#         if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
#             return True
#         else:
#             return False
=======

#Hi
class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
>>>>>>> 183596a7e0d04f9b438a82b5b037fa2c024376a6


def redrawWindow(win, game, p):
    win.fill(color = (138,51,36))

    if not (game.connected()):
        win.blit(bg_loading, (0, 0))
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (width / 3 - 90, height / 2 + 150))
    else:
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1, (255,211,155))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (255,211,155))
        win.blit(text, (400, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (420, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 150, 150, (50, 500), 5), Button("Scissors", 150, 150, (250, 500), 5),
        Button("Paper", 150, 150, (450, 500), 5)]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    start_btn = Button('Start', 200, 40, (width / 2 - 100, height / 2 + 150), 5)
    # Opening screen
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        # font = pygame.font.SysFont("comicsans", 60)
        # text = font.render("Click to Play!", 1, (255, 0, 0))
        # INSIDE OF THE GAME LOOP
        win.blit(bg, (0, 0))
        start_btn.draw(win)
        # win.blit(text, (width/3 - 50, height/2 + 150))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu_screen()
