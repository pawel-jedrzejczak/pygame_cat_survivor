import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

SCREENSIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768
camera_x = 0
camera_y = 0

screen = pygame.display.set_mode(SCREENSIZE, flags=pygame.SCALED, vsync=1)
pygame.display.set_caption("Catnip Survivors")
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# wczytanie grafik
path = os.path.join(os.pardir, 'images')  # lub w zaleznosci od wlasnej struktury folderow w projekcie: os.getcwd()
file_names = sorted(os.listdir(path))
BACKGROUND = pygame.image.load(os.path.join(path, 'zone.png')).convert()
file_names.remove('zone.png')
IMAGES = {}  # slownik w postaci:
# klucz - nazwa pliku bez rozszerzenia '.png' wielkimi literami,
# wartosc - zaladowany przez pygame obraz
for file_name in file_names:
    image_name = file_name[:-4].upper()
    IMAGES[image_name] = pygame.image.load(os.path.join(path, file_name)).convert_alpha(BACKGROUND)

# wczytanie dźwięków
sfx_path = os.path.join(os.pardir, 'sounds')
file_names = sorted(os.listdir(sfx_path))
SOUNDS = {}
for file_name in file_names:
    sfx_name = file_name[:-4].upper()
    SOUNDS[sfx_name] = str(os.path.join(sfx_path, file_name))
pygame.mixer.music.load(SOUNDS['BGM'])
pygame.mixer.music.set_volume(0.4)

set_of_expdrop = pygame.sprite.Group()  # zbiór wszystkich punktów doświadczenia leżących na ekranie
set_of_enemies = pygame.sprite.Group() # zbiór w którym sa wszyscy wrogrowie na ekranie


def get_game_time(from_when):
    return (pygame.time.get_ticks() - from_when) / 1000


class Text:
    def __init__(self, text, text_colour, pos_x, pos_y, font_type=None, font_size=74):
        self.text = str(text)
        self.font = pygame.font.SysFont(font_type, font_size,)
        self.color = text_colour
        self.image = self.font.render(self.text, True, text_colour)
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y

    def draw(self, surface):
        self.image = self.font.render(self.text, True, self.color)
        surface.blit(self.image, self.rect)


class Button:
    def __init__(self, text, pos_x, pos_y):
        self.image = IMAGES['BUTTON1']
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.text = Text(text, (255, 255, 255), self.rect.center[0], self.rect.center[1], font_size=76)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.text.draw(surface)


class UpgradeButton:
    def __init__(self, text_type, text_description, pos_x, pos_y):
        self.image = IMAGES['BUTTON2']
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.text = Text(text_type, (20, 20, 0), self.rect.center[0], self.rect.center[1]-30, font_size=44)
        self.text2 = Text(text_description, (0, 0, 0), self.rect.center[0], self.rect.center[1] + 8, font_size=36)
        self.text.rect.left = self.rect.center[0] - 400
        self.text2.rect.left = self.rect.center[0] - 390

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.text.draw(surface)
        self.text2.draw(surface)


# klasa punktów doświadczenia upuszczanych przez wrogów
class ExperienceDrop(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = IMAGES['EXP']
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y

    def update(self, surface):
        self.draw(surface)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.center[0] - camera_x, self.rect.center[1] - camera_y))
