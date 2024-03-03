import pygame
import system as my_system


# podstawowa klasa wroga z której dziedziczy każdy wróg
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.health = 1
        self.max_health = self.health
        self.movement_speed = 1
        self.strength = 1

        self.sprites = []
        self.sprites.append(my_system.IMAGES['WOLF1'])
        self.sprites.append(my_system.IMAGES['BEAR1'])
        self.animation_frame = 0
        self.frame_timer = 0
        self.animation_delay = 0.5

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.is_flipped = False
        self.direction = pygame.math.Vector2((my_system.camera_x,my_system.camera_y)) - pygame.math.Vector2(self.rect.center)
        self.time_since_last_dmg = 0

    def move(self, direction):
        if direction[0] < 0:
            self.is_flipped = True
        else:
            self.is_flipped = False
        direction.normalize_ip()  # normalizacja daje jednostkowy wektor kierunku
        self.rect.center += direction * self.movement_speed

    def update(self, player):
        self.direction = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        self.time_since_last_dmg += my_system.clock.get_time() / 1000

        if self.direction.length() > 42.0:
            # obsługa animacji
            self.frame_timer += my_system.clock.get_time() / 1000
            if self.frame_timer >= self.animation_delay:
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites)
                self.frame_timer = 0

            self.move(self.direction)
        else:
            self.animation_frame = 0
            self.attack_player(player)

        if self.health < self.max_health:
            health_precentage = self.health/self.max_health
            pygame.draw.rect(my_system.screen, (255, 255, 255), pygame.Rect(self.rect.center[0] - my_system.camera_x, self.rect.top - my_system.camera_y + 8, self.rect[2], 8))
            pygame.draw.rect(my_system.screen, (0, 199, 9), pygame.Rect(self.rect.center[0] - my_system.camera_x, self.rect.top - my_system.camera_y + 8, self.rect[2]*health_precentage, 8))

        self.image = self.sprites[self.animation_frame]
        self.draw()

    def draw(self):
        my_system.screen.blit(pygame.transform.flip(self.image, self.is_flipped, False), (self.rect.center[0] - my_system.camera_x, self.rect.center[1] - my_system.camera_y))

    def attack_player(self, player):
        player.current_health -= self.strength / player.defense

    def damaged(self, dmg, knockback, immunity):
        temp = self.movement_speed
        self.movement_speed = knockback
        self.move(-self.direction)
        self.movement_speed = temp
        if self.time_since_last_dmg > immunity:
            self.health -= dmg
            self.time_since_last_dmg = 0

    def __del__(self):
        my_system.set_of_expdrop.add(my_system.ExperienceDrop(self.rect.center[0], self.rect.center[1]))


class EnemyDog(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 12
        self.movement_speed = 2
        self.strength = 2

        self.sprites = []
        self.sprites.append(my_system.IMAGES['WOLF1'])
        self.sprites.append(my_system.IMAGES['WOLF2'])
        self.sprites.append(my_system.IMAGES['WOLF3'])
        self.sprites.append(my_system.IMAGES['WOLF4'])
        self.animation_delay = 0.1

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health


class EnemyBear(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 30
        self.movement_speed = 1
        self.strength = 9

        self.sprites = []
        self.sprites.append(my_system.IMAGES['BEAR1'])
        self.sprites.append(my_system.IMAGES['BEAR2'])
        self.sprites.append(my_system.IMAGES['BEAR3'])
        self.sprites.append(my_system.IMAGES['BEAR4'])
        self.animation_delay = 0.2

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health


class EnemySnake(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 17
        self.movement_speed = 3
        self.strength = 4

        self.sprites = []
        self.sprites.append(my_system.IMAGES['SNAKE1'])
        self.sprites.append(my_system.IMAGES['SNAKE2'])
        self.sprites.append(my_system.IMAGES['SNAKE3'])
        self.sprites.append(my_system.IMAGES['SNAKE4'])
        self.sprites.append(my_system.IMAGES['SNAKE5'])
        self.sprites.append(my_system.IMAGES['SNAKE6'])
        self.sprites.append(my_system.IMAGES['SNAKE7'])
        self.sprites.append(my_system.IMAGES['SNAKE8'])
        self.animation_delay = 0.1

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health


class EnemyBird(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 6
        self.movement_speed = 6
        self.strength = 1

        self.sprites = []
        self.sprites.append(my_system.IMAGES['BIRD1'])
        self.sprites.append(my_system.IMAGES['BIRD2'])
        self.sprites.append(my_system.IMAGES['BIRD3'])
        self.sprites.append(my_system.IMAGES['BIRD4'])
        self.animation_delay = 0.05

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health


class EnemyAlphaWolf(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 26
        self.movement_speed = 3
        self.strength = 6

        self.sprites = []
        self.sprites.append(my_system.IMAGES['WOLFB_1'])
        self.sprites.append(my_system.IMAGES['WOLFB_2'])
        self.sprites.append(my_system.IMAGES['WOLFB_3'])
        self.sprites.append(my_system.IMAGES['WOLFB_4'])
        self.animation_delay = 0.09

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health


class EnemyCatto(Enemy):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.health = 30
        self.movement_speed = 4
        self.strength = 9

        self.sprites = []
        self.sprites.append(my_system.IMAGES['CAT1'])
        self.sprites.append(my_system.IMAGES['CAT2'])
        self.sprites.append(my_system.IMAGES['CAT3'])
        self.sprites.append(my_system.IMAGES['CAT4'])
        self.animation_delay = 0.1

        self.image = self.sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = pos_x, pos_y
        self.max_health = self.health
