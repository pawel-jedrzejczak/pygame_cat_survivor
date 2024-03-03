import pygame
import system as my_system
import random


# klasa whip(podstawowa broń)
class Whip(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = my_system.IMAGES['WEAPON_WHIP']
        self.delay = 0
        self.player = player
        self.strength = 2 * player.strength
        self.knockback = 30
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['WHIP']))

    def update(self):
        self.delay += my_system.clock.get_time() / 1000
        if self.delay < 0.11:
            self.rect.center = (self.player.rect.center[0] + 660 * self.delay, self.player.rect.center[1] - 20)
            my_system.screen.blit(self.image, (self.rect.center[0] - my_system.camera_x , self.rect.center[1] - my_system.camera_y))
        elif self.delay < 0.22:
            self.rect.center = (self.player.rect.center[0] - 1000 * self.delay, self.player.rect.center[1] - 20)
            my_system.screen.blit(pygame.transform.flip(self.image, True, True), (self.rect.center[0] - my_system.camera_x , self.rect.center[1] - my_system.camera_y))
        else:
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['WHIP']))
            self.player.weapons_in_use.remove(self)
        for enemy in my_system.set_of_enemies:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.damaged(self.strength, self.knockback, 0.6)


class MagicWand(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = my_system.IMAGES['WEAPON_WAND']
        self.direction = None
        self.player = player
        self.strength = 1.4 * player.strength
        self.knockback = 1
        self.speed = 7
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['WAND']))
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.direction is None:
            for enemy in my_system.set_of_enemies:
                if random.randint(1,4) == 3:
                    self.direction = enemy.direction
                    self.direction.normalize_ip()
                    self.direction[0] *= -1
                    self.direction[1] *= -1
        else:
            self.rect.center += self.direction * self.speed
            for enemy in my_system.set_of_enemies:
                if pygame.sprite.collide_rect(self, enemy):
                    enemy.damaged(self.strength, self.knockback, 0.6)

            my_system.screen.blit(pygame.transform.flip(self.image,random.randint(0, 1), random.randint(0, 1)), (self.rect.center[0] - my_system.camera_x, self.rect.center[1] - my_system.camera_y))
        if my_system.get_game_time(self.start_time) > 10:
            self.player.weapons_in_use.remove(self)


class FireWisp(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.strength = 1 * player.strength
        self.knockback = 0

        self.sprites = []
        self.sprites.append(my_system.IMAGES['FIRE1'])
        self.sprites.append(my_system.IMAGES['FIRE2'])
        self.sprites.append(my_system.IMAGES['FIRE3'])
        self.sprites.append(my_system.IMAGES['FIRE4'])
        self.sprites.append(my_system.IMAGES['FIRE5'])
        self.sprites.append(my_system.IMAGES['FIRE6'])
        self.animation_frame = 0
        self.frame_timer = 0
        self.animation_delay = 0.1
        self.amount_of_frames = 6

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (player.rect.center[0]+random.randint(-600, 600), player.rect.center[1]+random.randint(-250, 250))
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['FIRE']))
        self.start_time = 0

    def update(self):
        for enemy in my_system.set_of_enemies:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.damaged(self.strength, self.knockback, 0.14)
        self.frame_timer += my_system.clock.get_time() / 1000
        self.start_time += my_system.clock.get_time() / 1000
        if self.frame_timer >= self.animation_delay:
            self.animation_frame = (self.animation_frame + 1) % self.amount_of_frames
            self.frame_timer = 0
        self.image = self.sprites[self.animation_frame]
        my_system.screen.blit(self.image, (self.rect.center[0] - my_system.camera_x, self.rect.center[1] - my_system.camera_y))
        if self.start_time > 3:
            self.player.weapons_in_use.remove(self)

