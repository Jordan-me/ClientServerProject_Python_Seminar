import pygame
import vlc


class Button:
    def __init__(self, text, width, height, pos, elevation, audio=None, image=None, top_color='#475F77',
                 bottom_color='#354B5E'):
        # Core attributes
        self.gui_font = pygame.font.Font(None, 30)
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]
        self.original_x_pos = pos[0]
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.audio = audio

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = top_color

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = bottom_color
        # text
        self.text_surf = self.gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=150)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=150)
        if self.image is None:
            screen.blit(self.text_surf, self.text_rect)
        else:
            screen.blit(self.image, (self.original_x_pos, self.original_y_pos))
        self.check_click()

    def check_click(self, top_color='#D9933A', top_color2='#475F77'):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = top_color
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = top_color2

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.original_x_pos <= x1 <= self.original_x_pos + self.width and self.original_y_pos <= y1 <= self.original_y_pos + self.height:
            vlc.libvlc_media_player_set_position(self.audio, 0.0)
            self.audio.play()
            return True
        else:
            return False
