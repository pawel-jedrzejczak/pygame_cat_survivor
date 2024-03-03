import pygame
import system as my_system
import weapons as my_weapons


# klasa gracza
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # parametry gracza
        self.max_health = 1000
        self.current_health = 1000
        self.defense = 3
        self.movement_speed = 4
        self.experience = 0
        self.total_exp = 0
        self.exp_to_next_level = 10
        self.level = 1
        self.max_level = 14
        self.strength = 2

        #animacje
        self.idle = True
        self.idle_sprites = []
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE1'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE2'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE3'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE4'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE5'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE6'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE7'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE8'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE9'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE10'])
        self.idle_sprites.append(my_system.IMAGES['PLAYER_IDLE11'])
        self.run_sprites = []
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN1'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN2'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN3'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN4'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN5'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN6'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN7'])
        self.run_sprites.append(my_system.IMAGES['PLAYER_RUN8'])
        self.animation_frame = 0
        self.frame_timer = 0
        self.animation_delay = 0.4
        self.amount_of_frames = 11

        # inicjalizacja rzeczy które nie są statystykami(taki 'backend')
        self.image = self.idle_sprites[self.animation_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (my_system.SCREEN_WIDTH - self.rect[2]) // 2, (my_system.SCREEN_HEIGHT - self.rect[3]) // 2
        self.chunk_x = -1
        self.chunk_y = -1
        self.is_flipped = False
        self.weapons_in_use = pygame.sprite.Group()
        self.upgrade_window = False
        self.upgrades_to_use = ["Movement Speed Upgrade","Movement Speed Upgrade","Attack Speed Upgrade","Attack Speed Upgrade","Power Upgrade","Power Upgrade","New Weapon - Magic Wand","New Weapon - Fire Wisp","Defense Upgrade","Defense Upgrade","Max Health Increase","Max Health Increase","Max Health Increase","Restore Full Health","Restore Full Health"]

        # paraemtry posiadania i opóźnienia broni
        self.weapon_whip_obtained = True
        self.whip_delay = 3
        self.whip_timer = 0

        self.weapon_wand_obtained = False
        self.wand_delay = 4
        self.wand_timer = 0

        self.weapon_wisp_obtained = False
        self.wisp_delay = 13
        self.wisp_timer = 0

    def _handle_events(self, keys_pressed):  # obsługa poruszania się gracza
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.set_run_state()
            self.rect.move_ip([-self.movement_speed, 0])
            my_system.camera_x -= self.movement_speed
            self.is_flipped = True
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.set_run_state()
            self.rect.move_ip([self.movement_speed, 0])
            my_system.camera_x += self.movement_speed
            self.is_flipped = False
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            self.set_run_state()
            self.rect.move_ip([0, -self.movement_speed])
            my_system.camera_y -= self.movement_speed
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            self.set_run_state()
            self.rect.move_ip([0, self.movement_speed])
            my_system.camera_y += self.movement_speed
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d] or keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w] or keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) is False:
            if self.idle is False:
                self.animation_frame = 0
                self.frame_timer = 0
                self.idle = True
                self.amount_of_frames = 11
                self.animation_delay = 0.4

    def update(self, keys_pressed):
        self._handle_events(keys_pressed)

        # obsługa animacji ---
        self.frame_timer += my_system.clock.get_time() / 1000
        if self.frame_timer >= self.animation_delay:
            self.animation_frame = (self.animation_frame + 1) % self.amount_of_frames
            self.frame_timer = 0

        if self.idle is True:
            self.image = self.idle_sprites[self.animation_frame]
        else:
            self.image = self.run_sprites[self.animation_frame]
        # --- koniec animacji

        # Broń bicz
        if self.weapon_whip_obtained:
            self.whip_timer += my_system.clock.get_time() / 1000
            if self.whip_timer > self.whip_delay:
                self.whip_timer = 0
                self.weapons_in_use.add(my_weapons.Whip(self))

        # Broń różdżka
        if self.weapon_wand_obtained:
            self.wand_timer += my_system.clock.get_time() / 1000
            if self.wand_timer > self.wand_delay:
                self.wand_timer = 0
                self.weapons_in_use.add(my_weapons.MagicWand(self))

        if self.weapon_wisp_obtained:
            self.wand_timer += my_system.clock.get_time() / 1000
            if self.wand_timer > self.wand_delay:
                self.wand_timer = 0
                self.weapons_in_use.add(my_weapons.FireWisp(self))

        self.weapons_in_use.update()

        # obsługa podnoszenia punktów doświadczenia ---
        for exp in my_system.set_of_expdrop:
            if pygame.sprite.collide_rect(self, exp):
                my_system.set_of_expdrop.remove(exp)
                self.experience += 4
                self.total_exp += 4
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['EXP']))

        if self.experience >= self.exp_to_next_level:
            self.level_up()
        # --- zakończona zwiększaniem poziomu

    def set_run_state(self):  # zmiana animacji pomiędzy bieganiem a spoczynkiem
        if self.idle is True:
            self.animation_frame = 0
            self.frame_timer = 0
            self.idle = False
            self.amount_of_frames = 8
            self.animation_delay = 0.1

    def level_up(self):  # obsługa zwiększania poziomu
        self.level += 1
        self.experience -= self.exp_to_next_level
        self.exp_to_next_level += self.level * 6
        if self.level <= self.max_level:
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['LEVEL_UP']))
            self.upgrade_window = True  # Zmiana tego parametru na True aktywuje pętle wyboru ulepszenia w main
        else:
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['HEAL']))
            self.current_health += (self.max_health - self.current_health) // 2

    def upgrade(self, index):
        if self.upgrades_to_use[index] == "Movement Speed Upgrade":
            self.movement_speed += 1
        elif self.upgrades_to_use[index] == "Attack Speed Upgrade":
            self.wand_delay -= 0.5
            self.whip_delay -= 0.6
            self.wisp_delay -= 0.7
        elif self.upgrades_to_use[index] == "Power Upgrade":
            self.strength += 2
        elif self.upgrades_to_use[index] == "New Weapon - Magic Wand":
            self.weapon_wand_obtained = True
        elif self.upgrades_to_use[index] == "Defense Upgrade":
            self.defense += 1
        elif self.upgrades_to_use[index] == "New Weapon - Fire Wisp":
            self.weapon_wisp_obtained = True
        elif self.upgrades_to_use[index] == "Max Health Increase":
            self.max_health += 200
            self.current_health += 200
        else:
            self.current_health = self.max_health
        pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['UPGRADE']))
        self.upgrade_window = False
        self.upgrades_to_use.pop(index)
