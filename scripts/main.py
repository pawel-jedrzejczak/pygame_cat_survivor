import pygame
import system as my_system
import player as my_player
import enemy_spawner as my_spawner
import random
import math

# inicjalizacja zmiennych
player = my_player.Player()
game_running = True
main_menu = True
game_started = False
game_over = False
new_record = False
upgrade_written = False
game_time = 0
continue_button = my_system.Button("Continue", my_system.SCREEN_WIDTH//2, my_system.SCREEN_HEIGHT//2)
new_game_button = my_system.Button("New game", my_system.SCREEN_WIDTH//2, my_system.SCREEN_HEIGHT//2 + 150)
exit_button = my_system.Button("Exit", my_system.SCREEN_WIDTH//2, my_system.SCREEN_HEIGHT//2 + 300)
game_over_button = my_system.Button("Back to menu", my_system.SCREEN_WIDTH//2, my_system.SCREEN_HEIGHT//2 + 150)
gameover_img = my_system.IMAGES['GAMEOVER']
logo = my_system.IMAGES['LOGO']
pause = my_system.IMAGES['PAUSE']
time_text = my_system.Text("00:00", (255, 255, 255), my_system.SCREEN_WIDTH//2, 20, font_size=48)
phase_text = my_system.Text("Phase 1", (255, 255, 255), my_system.SCREEN_WIDTH//2, 50, font_size=30)
new_record_text = my_system.Text("New record!", (255, 208, 16), my_system.SCREEN_WIDTH // 2, my_system.SCREEN_HEIGHT // 2 + 50, font_size=48)
highscore_text = my_system.Text("High score: 0", (255, 255, 255), 75, my_system.SCREEN_HEIGHT - 15, font_size=30)
end_text = "empty"


# ------- resetowanie wszystkich wartości do domyślnych po wciśnięciu nowej gry -------
def new_game():
    global main_menu
    global player
    global game_started
    global game_time

    game_started = True
    main_menu = False
    del player
    player = my_player.Player()
    my_system.set_of_enemies.empty()
    my_system.set_of_expdrop.empty()
    my_spawner.phase = 1
    my_spawner.time_from_last_spawn = pygame.time.get_ticks()
    my_spawner.time_from_phase_start = pygame.time.get_ticks()
    my_spawner.phase_length = 50
    my_system.camera_x = 0
    my_system.camera_y = 0
    my_system.start_time = pygame.time.get_ticks()
    game_time = 0
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)


while game_running:  # główna pętla gry

    while game_over:  # ------- obsługa pętli zakończenia gry(przegranej) -------
        my_system.screen.fill((0, 0, 0))
        game_over_button.draw(my_system.screen)
        my_system.screen.blit(gameover_img, (my_system.SCREEN_WIDTH // 2 - 570, my_system.SCREEN_HEIGHT // 2 - 256))
        end_text.draw(my_system.screen)
        if new_record:
            new_record_text.draw(my_system.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                main_menu = False
                game_over = False
            if pygame.mouse.get_pressed()[0] and game_over_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                game_started = False
                main_menu = True
                game_over = False
        pygame.display.flip()
        my_system.clock.tick(60)

    while main_menu:  # ------- pętla która obsługuje początkowe menu gry i pauze---------
        my_system.screen.fill((0, 0, 0))
        new_game_button.draw(my_system.screen)
        exit_button.draw(my_system.screen)
        if game_started:  # jeśli jest rozpoczęta nowa gra to ten if otwieram okno pauzy zamiast głównego menu
            my_system.screen.blit(pause, (my_system.SCREEN_WIDTH//2 - 307, my_system.SCREEN_HEIGHT//2 - 250))
            continue_button.draw(my_system.screen)
        else:
            my_system.screen.blit(logo, (33, my_system.SCREEN_HEIGHT // 2 - 200))
            f = open("highscore.txt", "r")
            highscore_text.text = str(f"High score: {f.readline()}")
            f.close()
            highscore_text.draw(my_system.screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                main_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_started:
                    pygame.mixer.music.unpause()
                    main_menu = False
            if pygame.mouse.get_pressed()[0] and new_game_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                new_game()
            if pygame.mouse.get_pressed()[0] and exit_button.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                game_running = False
                main_menu = False
            if pygame.mouse.get_pressed()[0] and continue_button.rect.collidepoint(pygame.mouse.get_pos()) and game_started and event.type == pygame.MOUSEBUTTONDOWN:
                main_menu = False
                pygame.mixer.music.unpause()
        pygame.display.flip()
        my_system.clock.tick(60)

    while player.upgrade_window:  # ------- pętla która obsługuje wybór ulepszeń kiedy gracz zdobędzie nowy poziom ---------
        if upgrade_written is False:  # funkcja if sprawdza czy przyciski zostały narysowane i rysuje je tylko raz(żeby zachować ich przeźroczystość)
            upgrade_descriptions = {
                "Movement Speed Upgrade": "Increases player's movement speed by 1",
                "Attack Speed Upgrade": "Reduces delay between player's attacks a bit",
                "Power Upgrade": "Increases all weapons' damage by 2",
                "New Weapon - Magic Wand": "Shoots lighting balls",
                "New Weapon - Fire Wisp": "Spawns at random location for few seconds",
                "Defense Upgrade": "Increases player's defense by 1",
                "Max Health Increase": "Increases player's max health by 200",
                "Restore Full Health": "Restores player's health to full (wow)"
            }
            up1 = random.randint(0, len(player.upgrades_to_use)-1)
            up2 = random.randint(0, len(player.upgrades_to_use)-1)
            while up2 == up1:
                up2 = random.randint(0, len(player.upgrades_to_use)-1)
            up3 = random.randint(0, len(player.upgrades_to_use)-1)
            while up3 == up1 or up3 == up2:
                up3 = random.randint(0, len(player.upgrades_to_use)-1)

            upgrade_1 = my_system.UpgradeButton(player.upgrades_to_use[up1], upgrade_descriptions[player.upgrades_to_use[up1]], my_system.SCREEN_WIDTH // 2, 200)
            upgrade_2 = my_system.UpgradeButton(player.upgrades_to_use[up2], upgrade_descriptions[player.upgrades_to_use[up2]], my_system.SCREEN_WIDTH // 2, 370)
            upgrade_3 = my_system.UpgradeButton(player.upgrades_to_use[up3], upgrade_descriptions[player.upgrades_to_use[up3]], my_system.SCREEN_WIDTH // 2, 540)
            levelup_text = my_system.Text("LEVEL UP! Choose upgrade",(255, 208, 16),my_system.SCREEN_WIDTH//2, my_system.SCREEN_HEIGHT - 80,font_size=80)
            upgrade_1.draw(my_system.screen)
            upgrade_2.draw(my_system.screen)
            upgrade_3.draw(my_system.screen)
            levelup_text.draw(my_system.screen)
        upgrade_written = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                main_menu = False
                game_over = False
                player.upgrade_window = False
            if pygame.mouse.get_pressed()[0] and upgrade_1.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                player.upgrade(up1)
                upgrade_written = False
            if pygame.mouse.get_pressed()[0] and upgrade_2.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                player.upgrade(up2)
                upgrade_written = False
            if pygame.mouse.get_pressed()[0] and upgrade_3.rect.collidepoint(pygame.mouse.get_pos()) and game_started and event.type == pygame.MOUSEBUTTONDOWN:
                player.upgrade(up3)
                upgrade_written = False
        pygame.display.flip()
        my_system.clock.tick(60)

# ------- główna pętla gry -------
    my_system.screen.fill((0, 0, 0))  # rysowanie planszy i postaci gracza
    my_system.screen.blit(my_system.BACKGROUND, (2048*math.floor(player.rect.center[0]/2048) - my_system.camera_x - 1000, 2048*math.floor(player.rect.center[1]/2048) - my_system.camera_y - 1000))
    my_system.screen.blit(pygame.transform.flip(player.image, player.is_flipped, False), (player.rect.center[0] - my_system.camera_x, player.rect.center[1] - my_system.camera_y))

    for event in pygame.event.get(): # obsługa wyłączania gry przez przycisk
        if event.type == pygame.QUIT:
            game_running = False
            main_menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['PAUSE']))
                pygame.mixer.music.pause()
                main_menu = True
            # if event.key == pygame.K_p: # dev tools
            #     my_spawner.phase_length = 1
            # if event.key == pygame.K_i:
            #     player.current_health = 0
            # if event.key == pygame.K_o:
            #     player.experience += 10
            #     player.total_exp += 10
            # if event.key == pygame.K_l:
            #     for enemy in my_spawner.set_of_enemies:
            #         my_spawner.set_of_enemies.remove(enemy)
            #         break

    if main_menu is False:  # sprawdzanie czy w tej samej 'klatce' nie wciśnięto klawisza pauzy, żeby uniknąć sytuacji wystąpienia gameover i pauzy naraz(w sumie to nie wiem czy to może się stać ale nie zaszkodzi się zabezpieczyć)
        my_spawner.update()
        player.update(pygame.key.get_pressed())
        my_system.set_of_enemies.update(player)
        my_system.set_of_expdrop.update(my_system.screen)
        # aktualizacja zegara na ekranie
        game_time += my_system.clock.get_time() / 1000
        mm, ss = divmod(int(game_time), 60)
        time_text.text = str("{:02d}:{:02d}".format(mm, ss))
        if player.current_health <= 0:  # sprawdzanie czy nastąpił gameover
            new_record = False
            total_score = int(game_time * player.total_exp * 0.1)
            f = open("highscore.txt", "r") # zapisywanie high score do pliku
            old_score = f.readline()
            f.close()
            if int(old_score) < total_score:
                new_record = True
                f = open("highscore.txt", "w")
                f.write(str(total_score))
                f.close()
            end_text = my_system.Text(f"Your time: {time_text.text}    Experience: {player.total_exp}    Total score: {total_score}", (255, 255, 255), my_system.SCREEN_WIDTH // 2, my_system.SCREEN_HEIGHT // 2, font_size=40)
            pygame.mixer.find_channel(True).play(pygame.mixer.Sound(my_system.SOUNDS['GAMEOVER']))
            pygame.mixer.music.pause()
            game_over = True
    # rysowanie paska zdrowia
    health_precentage = player.current_health / player.max_health
    pygame.draw.rect(my_system.screen, (255, 255, 255), pygame.Rect(0, my_system.SCREEN_HEIGHT - 8, my_system.SCREEN_WIDTH, 8))
    pygame.draw.rect(my_system.screen, (0, 199, 9), pygame.Rect(0, my_system.SCREEN_HEIGHT - 8, my_system.SCREEN_WIDTH * health_precentage, 8))
    # rysowanie paska doświadczenia
    exp_precentage = player.experience / player.exp_to_next_level
    pygame.draw.rect(my_system.screen, (0, 0, 0), pygame.Rect(0, my_system.SCREEN_HEIGHT - 16, my_system.SCREEN_WIDTH, 8))
    pygame.draw.rect(my_system.screen, (74, 158, 223), pygame.Rect(0, my_system.SCREEN_HEIGHT - 16, my_system.SCREEN_WIDTH * exp_precentage, 8))
    # wypisanie zegara i licznika fal wrogów
    time_text.draw(my_system.screen)
    phase_text.text = str(f"Phase {my_spawner.phase}")
    phase_text.draw(my_system.screen)
    pygame.display.flip()
    my_system.clock.tick(60)

pygame.quit()
