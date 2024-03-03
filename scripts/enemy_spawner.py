import pygame
import system as my_system
import enemy as my_enemy
import random

time_from_last_spawn = pygame.time.get_ticks()
time_from_phase_start = pygame.time.get_ticks()
phase_length = 30
phase = 1


def get_spawn_coords():  # funkcja generująca położenie w którym zespawnuje się nowy wróg
    side = random.randint(1, 4)
    if side == 1:
        return -150, random.randint(-10, my_system.SCREEN_HEIGHT+10)
    elif side == 2:
        return random.randint(-15, my_system.SCREEN_WIDTH+15), -150
    elif side == 3:
        return my_system.SCREEN_WIDTH + 150, random.randint(-10, my_system.SCREEN_HEIGHT+10)
    else:
        return random.randint(-15, my_system.SCREEN_WIDTH+15), my_system.SCREEN_HEIGHT+150


def spawn(enemy_choice):  # funckja spawnująca wroga do gry
    spawn_coords = get_spawn_coords()
    my_system.set_of_enemies.add(enemy_choice(spawn_coords[0] + my_system.camera_x, spawn_coords[1] + my_system.camera_y))


def next_phase(new_p_len):  # zmiana fali wrogów na kolejną
    global time_from_phase_start
    global phase
    global phase_length

    time_from_phase_start = pygame.time.get_ticks()
    phase += 1
    phase_length = new_p_len


def update():  # funkcja która obsługuje cały system spawnowania; fale wrogów itd.
    global phase
    global time_from_last_spawn
    global time_from_phase_start
    global phase_length

    for enemy in my_system.set_of_enemies:
        if enemy.health <= 0:
            my_system.set_of_enemies.remove(enemy)

    if phase == 1:
        if my_system.get_game_time(time_from_last_spawn) > 1.1:
            spawn(my_enemy.EnemyDog)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 2:
        if my_system.get_game_time(time_from_last_spawn) > 0.4:
            if random.randint(1, 50) == 40:
                spawn(my_enemy.EnemyBird)
            else:
                spawn(my_enemy.EnemyDog)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 3:
        if my_system.get_game_time(time_from_last_spawn) > 0.3:
            if random.randint(1, 12) == 5:
                if random.randint(1, 3) == 2:
                    spawn(my_enemy.EnemySnake)
                else:
                    spawn(my_enemy.EnemyBird)
            else:
                spawn(my_enemy.EnemyDog)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 4:
        if my_system.get_game_time(time_from_last_spawn) > 0.2:
            if random.randint(1, 4) == 1:
                if random.randint(1, 3) == 1:
                    spawn(my_enemy.EnemyBear)
                else:
                    spawn(my_enemy.EnemySnake)
            else:
                spawn(my_enemy.EnemyBird)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 5:
        if my_system.get_game_time(time_from_last_spawn) > 0.45:
            if random.randint(1, 2) == 1:
                if random.randint(1, 3) == 1:
                    spawn(my_enemy.EnemyBear)
                else:
                    spawn(my_enemy.EnemySnake)
            else:
                spawn(my_enemy.EnemyAlphaWolf)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 6:
        if my_system.get_game_time(time_from_last_spawn) > 0.45:
            if random.randint(1, 2) == 1:
                if random.randint(1, 2) == 1:
                    spawn(my_enemy.EnemyBear)
                else:
                    spawn(my_enemy.EnemyCatto)
            else:
                spawn(my_enemy.EnemyAlphaWolf)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 7:
        if my_system.get_game_time(time_from_last_spawn) > 0.14:
            pick = random.randint(1,7)
            if pick == 1:
                spawn(my_enemy.EnemyDog)
            elif pick == 2:
                spawn(my_enemy.EnemyBird)
            elif pick == 3:
                spawn(my_enemy.EnemyBear)
            elif pick == 4:
                spawn(my_enemy.EnemyCatto)
            elif pick == 5:
                spawn(my_enemy.EnemyAlphaWolf)
            else:
                spawn(my_enemy.EnemySnake)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    elif phase == 8:
        if my_system.get_game_time(time_from_last_spawn) > 0.04:
            pick = random.randint(1, 5)
            if pick == 1:
                spawn(my_enemy.EnemySnake)
            elif pick == 2:
                spawn(my_enemy.EnemyBird)
            elif pick == 3:
                spawn(my_enemy.EnemyBear)
            elif pick == 4:
                spawn(my_enemy.EnemyCatto)
            elif pick == 5:
                spawn(my_enemy.EnemyAlphaWolf)
            time_from_last_spawn = pygame.time.get_ticks()

        if my_system.get_game_time(time_from_phase_start) > phase_length:
            next_phase(30)

    else:
        if my_system.get_game_time(time_from_last_spawn) > 0.01:
            pick = random.randint(1, 5)
            if pick == 1:
                spawn(my_enemy.EnemySnake)
            elif pick == 2:
                spawn(my_enemy.EnemyBird)
            elif pick == 3:
                spawn(my_enemy.EnemyBear)
            elif pick == 4:
                spawn(my_enemy.EnemyCatto)
            elif pick == 5:
                spawn(my_enemy.EnemyAlphaWolf)
            time_from_last_spawn = pygame.time.get_ticks()
