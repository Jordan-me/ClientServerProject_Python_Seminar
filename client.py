import os

import pygame
import vlc

from network import Network
from Button import Button
import pickle


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = pygame.image.load(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


# Setup for sounds, defaults are good
pygame.mixer.init()
loading_sound = vlc.MediaPlayer("assets/audio/music_zapsplat_astro_race.mp3")
loading_sound.audio_set_volume(80)

pygame.font.init()
value = 0
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

bg = pygame.image.load("assets/menuScreen3.jpg")
bg = pygame.transform.scale(bg, (width, height))
bg_loading = pygame.transform.scale(pygame.image.load("assets/waitScreen.gif"), (width, height))
bg_loading_sprite = load_images_from_folder("assets/loading_frames")


def create_loading_animation(win, images,text = None, x=700, y=700):
    # Setting the framerate to 3fps just
    # to see the result properly
    if text is not None:
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render(text, 1, (0, 0, 0))

    for image in images:
        image = pygame.transform.scale(image, (x, y))
        win.blit(image, (0, 0))
        if text is not None:
            win.blit(text, (width / 3 - 30, height / 2 + 150))
        pygame.display.update()
        pygame.time.Clock().tick(50)


def redrawWindow(win, game, p):
    win.fill(color=(138, 51, 36))

    if not (game.connected()):
        create_loading_animation(win, bg_loading_sprite,text="Waiting for Player...")
        win.blit(pygame.transform.scale(bg_loading_sprite[-1], (width, height)), (0, 0))

    else:
        loading_sound.stop()
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Your Move", 1, (255, 211, 155))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (255, 211, 155))
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
    loading_sound.play()

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

    pygame.mixer.music.stop()
    loading_sound.stop()
    pygame.mixer.quit()


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
