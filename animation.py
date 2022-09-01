import os

import pygame


class Animation:
    def __init__(self, path,red = None):
        self.path = path
        self.images = []
        # self.red_timer = pygame.image.load("assets/timer/end_timer.png")
        # self.blue_timer = pygame.image.load("assets/timer/base_clock.png")
        self.red = red
        self.load_images_from_folder()


    def load_images_from_folder(self):
        for filename in os.listdir(self.path):
            img = pygame.image.load(os.path.join(self.path, filename))
            if img is not None:
                if self.red is not None and self.red is True:
                    self.images.append(self.red_timer)
                if self.red is not None and self.red is False:
                    self.images.append(self.blue_timer)
                self.images.append(img)

    def create_loading_animation(self, screen, width, height, delay=50, text=None, x_scale=700, y_scale=700,
                                 pos=(0, 0)):
        # Setting the framerate to 3fps just
        # to see the result properly
        if text is not None:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(text, 1, (0, 0, 0))

        for image in self.images:
            image = pygame.transform.scale(image, (x_scale, y_scale))
            screen.blit(image, pos)
            if text is not None:
                screen.blit(text, (width / 3 - 30, height / 2 + 150))
            pygame.display.update()
            pygame.time.Clock().tick(delay)
