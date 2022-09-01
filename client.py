import os
import random

import pygame
import vlc
from pygame import time

from InputBox import InputBox
from network import Network
from Button import Button
from animation import Animation
from timer import Timer
import pickle

your_name = ""
opponent_name = ""
your_choice = ""
opponent_choice = ""
your_score = 0
opponent_score = 0

# Setup for sounds, defaults are good
pygame.mixer.init()
loading_sound = vlc.MediaPlayer("assets/audio/music_zapsplat_astro_race.mp3")
loading_sound.audio_set_volume(80)
# sounds effect
rock_sound = vlc.MediaPlayer("assets/audio/rocks_sound.mp3")
rock_sound.audio_set_volume(80)
paper_sound = vlc.MediaPlayer("assets/audio/paper_sound.mp3")
paper_sound.audio_set_volume(110)
scissors_sound = vlc.MediaPlayer("assets/audio/scissors_sound.mp3")
scissors_sound.audio_set_volume(80)

pygame.font.init()
value = 0
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# images
bg = pygame.image.load("assets/menuScreen3.jpg")
bg = pygame.transform.scale(bg, (width, height))
bg_loading = pygame.transform.scale(pygame.image.load("assets/waitScreen.gif"), (width, height))
bg_loading_sprite = Animation("assets/loading_frames")
banner_image = pygame.image.load("assets/Banner_Title.png")
banner_image = pygame.transform.scale(banner_image, (width, 150))
lock_image = pygame.image.load("assets/lock.png")
lock_image = pygame.transform.scale(lock_image, (150, 150))

# crowns
winner_crown = pygame.image.load("assets/winner_crown.png")
loser_crown = pygame.image.load("assets/loser_crown.png")
# rps images
rock = pygame.image.load("assets/rock.png")
paper = pygame.image.load("assets/paper.png")
scissors = pygame.image.load("assets/scissors.png")


def get_btn(move):
    for btn in btns:
        if move == btn.text:
            return btn


def winner_window(window, game, p):
    window.fill(color=(135, 206, 255))


def loser_window(window, game, p):
    window.fill(color=(135, 206, 255))


def redrawWindow(window, game, p):
    window.fill(color=(135, 206, 255))
    if not (game.connected()):
        bg_loading_sprite.create_loading_animation(window, width, height, text="Waiting for Player...")
        window.blit(pygame.transform.scale(bg_loading_sprite.images[-1], (width, height)), (0, 0))

    else:
        # stop waiting sound
        loading_sound.stop()
        op = 0 if p == 1 else 1
        # names & scores
        window.blit(banner_image, (0, -20))
        font_names = pygame.font.SysFont("comicsans", 48)
        text_name = font_names.render(your_name + ':  ' + str(game.wins[p]), 1, (0, 0, 0))
        window.blit(text_name, (70, 150))
        text_opp_name = font_names.render(opponent_name + ':  ' + str(game.wins[op]), 1, (0, 0, 0))
        window.blit(text_opp_name, (width - 280, 150))

        if not game.isTie(p, op):
            if game.isWinner(p, op):
                window.blit(winner_crown, (25, 75))
                window.blit(loser_crown, (width - 275, 125))

            else:
                window.blit(loser_crown, (50, 125))
                window.blit(winner_crown, (width - 318, 75))

        font = pygame.font.SysFont("comicsans", 40)
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            print("I got the moves : ", move1, move2)
            text1 = get_btn(move1).image
            text2 = get_btn(move2).image
        else:
            if game.p1Went and p == 0:  # p = 0 and he chose
                # do animation of the move
                text1 = get_btn(move1).image

            elif game.p1Went:  # p = 1 and p = 0 chose
                # show animation of wondering
                # text1 = font.render("Locked In", 1, (0, 0, 0))
                text1 = lock_image
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                # do animation of the move
                text2 = get_btn(move2).image
            elif game.p2Went:
                # text2 = font.render("Locked In", 1, (0, 0, 0))
                text2 = lock_image
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            window.blit(text2, (100, 250))
            window.blit(text1, (400, 250))
        else:
            window.blit(text1, (100, 250))
            window.blit(text2, (420, 250))

        for btn in btns:
            btn.draw(window)

    pygame.display.update()


btns = [Button("Rock", 150, 150, (50, 500), 5, audio=rock_sound, image=rock),
        Button("Scissors", 150, 150, (250, 500), 5, audio=scissors_sound, image=scissors),
        Button("Paper", 150, 150, (450, 500), 5, audio=paper_sound, image=paper)]


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
                n.send("W" + str(player))
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
                    btn.audio.stop()
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
