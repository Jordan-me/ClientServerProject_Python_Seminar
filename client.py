import os

import pygame
import vlc

from InputBox import InputBox
from network import Network
from Button import Button
import pickle

your_name = ""
opponent_name = ""
your_choice = ""
opponent_choice = ""
TOTAL_NO_OF_ROUNDS = 5
your_score = 0
opponent_score = 0


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


def create_loading_animation(win, images, text=None, x=700, y=700):
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
        create_loading_animation(win, bg_loading_sprite, text="Waiting for Player...")
        win.blit(pygame.transform.scale(bg_loading_sprite[-1], (width, height)), (0, 0))

    else:
        # stop waiting sound
        loading_sound.stop()

        # names & scores
        font_names = pygame.font.SysFont("comicsans", 28)
        text_name = font_names.render(your_name + ':  ' + str(game.wins[p]), 1, (0, 0, 0))
        win.blit(text_name, (20, 50))
        text_opp_name = font_names.render(opponent_name + ':  ' + str(game.wins[0 if p == 1 else 1]), 1, (0, 0, 0))
        win.blit(text_opp_name, (width - 250, 50))

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
    global opponent_name
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    try:
        game = n.send("N" + your_name)
    except:
        print("Couldn't get game")

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
        opponent_name = game.p1Name if player == 1 else game.p2Name
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
    global your_name
    run = True
    clock = pygame.time.Clock()
    start_btn = Button('Start', 200, 40, (width / 2 - 100, height / 2 + 150), 5)
    input_box = InputBox(100, 55, 140, 32)
    font = pygame.font.SysFont("comicsans", 24)
    msg_text = "Enter Your Name!"
    # Opening screen
    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        label_name = font.render("Name:", 1, (0, 0, 0))
        # INSIDE OF THE GAME LOOP
        win.blit(bg, (0, 0))
        start_btn.draw(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            input_box.handle_event(event)
            if start_btn.pressed and input_box.text == '':
                input_box.update_error()
                print("Enter Name!")
            if start_btn.pressed and input_box.text != '':
                your_name = input_box.text
                run = False

        win.blit(label_name, (10, 50))
        input_box.update()
        input_box.draw(win)
        pygame.display.update()

    main()


while True:
    menu_screen()
