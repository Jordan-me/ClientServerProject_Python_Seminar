import pygame
import vlc

from back.log_service import add_log_warnning, add_log_info
from front.widgets.InputBox import InputBox
from back.network import Network
from front.widgets.Button import Button
from front.widgets.animation import Animation
from timer import Timer


class Client():
    def __init__(self, name = ""):
        self.width = 700
        self.height = 700
        self.your_name = name
        self.your_choice = ""
        self.opponent_name = ""
        self.opponent_choice = ""
        self.your_score = 0
        self.opponent_score = 0
        # Setup for sounds, defaults are good
        pygame.mixer.init()
        self.loading_sound = vlc.MediaPlayer("assets/audio/music_zapsplat_astro_race.mp3")
        self.loading_sound.audio_set_volume(80)
        # sounds effect
        self.rock_sound = vlc.MediaPlayer("assets/audio/rocks_sound.mp3")
        self.rock_sound.audio_set_volume(80)
        self.paper_sound = vlc.MediaPlayer("assets/audio/paper_sound.mp3")
        self.paper_sound.audio_set_volume(110)
        self.scissors_sound = vlc.MediaPlayer("assets/audio/scissors_sound.mp3")
        self.scissors_sound.audio_set_volume(80)
        self.win_sound = vlc.MediaPlayer("assets/audio/win_sound.mp3")
        self.win_sound.audio_set_volume(80)
        self.lose_sound = vlc.MediaPlayer("assets/audio/lose_sound.mp3")
        self.lose_sound.audio_set_volume(80)

        # images
        self.bg = pygame.image.load("assets/menuScreen3.jpg")
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.bg_loading = pygame.transform.scale(pygame.image.load("assets/waitScreen.gif"), (self.width, self.height))
        self.bg_loading_sprite = Animation("assets/loading_frames")
        self.banner_image = pygame.image.load("assets/Banner_Title.png")
        self.banner_image = pygame.transform.scale(self.banner_image, (self.width, 150))
        self.lock_image = pygame.image.load("assets/lock.png")
        self.lock_image = pygame.transform.scale(self.lock_image, (150, 150))
        self.wait_sprite = Animation("assets/waiting_frames")
        self.lose_win_sprite = {"win": {"anim": [Animation("assets/win/sparkle_frames")],
                                        "images": [
                                            pygame.transform.scale(pygame.image.load("assets/win/congrats.png"),
                                                                   (self.width - 100, 150)),
                                            pygame.transform.scale(pygame.image.load("assets/win/cup.png"),
                                                                   (self.width - 200, 200))],
                                        "sound": self.win_sound
                                        },
                                "lose": {"anim": [Animation("assets/lose/loser_frames")],
                                         "images": [pygame.image.load("assets/lose/sign.png")],
                                         "sound": self.lose_sound}
                                }
        # crowns
        self.winner_crown = pygame.image.load("assets/winner_crown.png")
        self.loser_crown = pygame.image.load("assets/loser_crown.png")
        # rps images
        self.rock = pygame.image.load("assets/rock.png")
        self.paper = pygame.image.load("assets/paper.png")
        self.scissors = pygame.image.load("assets/scissors.png")
        self.btns = [Button("Rock", 150, 150, (50, 500), 5, audio=self.rock_sound, image=self.rock),
                     Button("Scissors", 150, 150, (250, 500), 5, audio=self.scissors_sound, image=self.scissors),
                     Button("Paper", 150, 150, (450, 500), 5, audio=self.paper_sound, image=self.paper)]
        self.run()

    def get_btn(self, move):
        for btn in self.btns:
            if move == btn.text:
                return btn

    def winner_lose_window(self, window, mode="win", pos_sign=(50, 150), pos2=(90, 350), pos_anim=(0, 0),
                           scale=(700, 700)):
        timer = Timer(5)
        played = False
        while timer.check_timer():
            self.lose_win_sprite[mode]["sound"].play()
            window.fill(color=(135, 206, 255))
            window.blit(self.banner_image, (0, -20))
            window.blit(self.lose_win_sprite[mode]["images"][0], pos_sign)
            if mode == "win":
                window.blit(self.lose_win_sprite[mode]["images"][1], pos2)
            pygame.display.update()
            self.lose_win_sprite[mode]["anim"][0].create_loading_animation(window, self.width, self.height, delay=20,
                                                                           x_scale=scale[0],
                                                                           y_scale=scale[1], pos=pos_anim)

        self.lose_win_sprite[mode]["sound"].stop()

    def redrawWindow(self, window, game, p):
        window.fill(color=(135, 206, 255))
        if not (game.connected()):
            self.bg_loading_sprite.create_loading_animation(window, self.width, self.height, text="Waiting for Player...")
            window.blit(pygame.transform.scale(self.bg_loading_sprite.images[-1], (self.width, self.height)), (0, 0))

        else:
            # stop waiting sound
            self.loading_sound.stop()
            op = 0 if p == 1 else 1
            # names & scores
            window.blit(self.banner_image, (0, -20))
            font_names = pygame.font.SysFont("comicsans", 48)
            text_name = font_names.render(self.your_name + ':  ' + str(game.wins[p]), 1, (0, 0, 0))
            window.blit(text_name, (70, 150))
            text_opp_name = font_names.render(self.opponent_name + ':  ' + str(game.wins[op]), 1, (0, 0, 0))
            window.blit(text_opp_name, (self.width - 280, 150))

            if not game.isTie(p, op):
                if game.isWinner(p, op):
                    window.blit(self.winner_crown, (25, 75))
                    window.blit(self.loser_crown, (self.width - 275, 125))

                else:
                    window.blit(self.loser_crown, (50, 125))
                    window.blit(self.winner_crown, (self.width - 318, 75))

            font = pygame.font.SysFont("comicsans", 40)
            move1 = game.get_player_move(0)
            move2 = game.get_player_move(1)
            if game.bothWent():
                text1 = self.get_btn(move1).image
                text2 = self.get_btn(move2).image
            else:
                if game.p1Went and p == 0:  # p = 0 and he chose
                    # do animation of the move
                    text1 = self.get_btn(move1).image

                elif game.p1Went:  # p = 1 and p = 0 chose
                    # show animation of wondering
                    text1 = self.lock_image
                else:
                    text1 = font.render("Waiting...", 1, (0, 0, 0))

                if game.p2Went and p == 1:
                    # do animation of the move
                    text2 = self.get_btn(move2).image
                elif game.p2Went:
                    text2 = self.lock_image
                else:
                    text2 = font.render("Waiting...", 1, (0, 0, 0))

            if p == 1:
                window.blit(text2, (100, 250))
                window.blit(text1, (400, 250))
            else:
                window.blit(text1, (100, 250))
                window.blit(text2, (420, 250))

            for btn in self.btns:
                btn.draw(window)

        pygame.display.update()

    def play(self, win):
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        try:
            game = n.send("N" + self.your_name)
            add_log_info("Client: play, sent name's player to server")
        except:
            add_log_warnning("Client: play, Couldn't get game")

        self.loading_sound.play()
        while run:
            clock.tick(60)
            try:
                game = n.send("get")
                add_log_info("Client: play, Got game from server")
                if game.close:
                    break
            except:
                run = False
                add_log_warnning("Client: play, Couldn't get game")
                break
            self.opponent_name = game.p1Name if player == 1 else game.p2Name
            if game.bothWent():
                self.redrawWindow(win, game, player)
                pygame.time.delay(500)
                try:
                    game = n.send("reset")
                    add_log_info("Client: play, send reset game request")
                except:
                    run = False
                    add_log_warnning("Client: play, Couldn't get game")
                    break

                font = pygame.font.SysFont("comicsans", 90)
                if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                    self.winner_lose_window(win, mode="win", pos_sign=(50, 150), pos2=(90, 350), pos_anim=(0, 0),
                                            scale=(700, 700))
                    n.send("W" + str(player))

                elif game.winner() == -1:
                    text = font.render("Tie Game!", 1, (255, 0, 0))
                    win.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(2000)
                else:
                    self.winner_lose_window(win, mode="lose", pos_sign=(40, 150), pos_anim=(250, 350), scale=(180, 180))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    add_log_info("Client: play, send QUIT request")
                    n.send('QUIT')
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in self.btns:
                        btn.audio.stop()
                        if not game.connected():
                            add_log_info("Client: play, the opponent has disconnected")
                            self.play(win)
                        if btn.click(pos) and game.connected():
                            if player == 0:
                                if not game.p1Went:
                                    n.send(btn.text)
                            else:
                                if not game.p2Went:
                                    n.send(btn.text)


            self.redrawWindow(win, game, player)

        pygame.mixer.music.stop()
        self.loading_sound.stop()
        pygame.mixer.quit()

    def run(self):
        pygame.font.init()
        win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Client")
        run = True if self.your_name == "" else False
        clock = pygame.time.Clock()
        start_btn = Button('Start', 200, 40, (self.width / 2 - 100, self.height / 2 + 150), 5)
        input_box = InputBox(100, 55, 140, 32)
        font = pygame.font.SysFont("comicsans", 24)
        msg_text = "Enter Your Name!"
        # Opening screen
        while run:
            clock.tick(60)
            win.fill((128, 128, 128))

            label_name = font.render("Name:", 1, (0, 0, 0))
            # INSIDE OF THE GAME LOOP
            win.blit(self.bg, (0, 0))
            start_btn.draw(win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                input_box.handle_event(event)
                if start_btn.pressed and input_box.text == '':
                    input_box.update_error()
                    add_log_info("Client: run, The input box empty, please enter a valid name")
                if start_btn.pressed and input_box.text != '':
                    self.your_name = input_box.text
                    run = False

            win.blit(label_name, (10, 50))
            input_box.update()
            input_box.draw(win)
            pygame.display.update()

        self.play(win)

if __name__ == "__main__":
    # when running client manually
    Client()
else:
    # when running server
    add_log_info("Client: client_main, entered to client.py file")