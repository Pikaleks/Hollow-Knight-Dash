#!/usr/bin/env python3

import pygame
import button

pygame.init()

# Créer la fenêtre de jeu
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

original_background_main_img = pygame.image.load("assets/images/Main_Menu.png").convert()
background_main_img = pygame.transform.scale(original_background_main_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

original_background_main_title = pygame.image.load("assets/images/Main_Title.png").convert_alpha()
background_main_title = pygame.transform.scale(original_background_main_title, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

original_background_main_title2 = pygame.image.load("assets/images/Main_Title2.png").convert_alpha()
background_main_title2 = pygame.transform.scale(original_background_main_title2, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

# Variables du jeu
game_paused = False
menu_state = "main"

# Définir les polices
font_size = 60
font_path = "assets/buttons/TrajanPro-Regular.ttf"
font = pygame.font.Font(font_path, font_size)

#font = pygame.font.SysFont("arialblack", font_size)

# Définir les couleurs
TEXT_COL = (255, 255, 255)

# Créer des instances de boutons centrées
resume_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 - 100, "Play", font, TEXT_COL, 1)
options_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 - 10, "Options", font, TEXT_COL, 1)
quit_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 + 80, "Quit", font, TEXT_COL, 1)
video_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 - 100, "Video", font, TEXT_COL, 1)
audio_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 - 10, "Audio", font, TEXT_COL, 1)
keys_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 + 80, "Keys", font, TEXT_COL, 1)
back_button = button.ButtonText(SCREEN_WIDTH / 90, SCREEN_HEIGHT / 2 + 170, "Back", font, TEXT_COL, 1)

run = True
show_title1 = True  # Variable pour suivre l'état d'affichage du titre 1
title_x = (SCREEN_WIDTH - background_main_title.get_width()) // 2
title2_x = (SCREEN_WIDTH - background_main_title2.get_width()) // 2

while run:
    screen.blit(background_main_img, (0, 0))

    # Vérifier si le jeu est en pause
    if game_paused:
        # Vérifier l'état du menu
        if menu_state == "main":
            # Dessiner les boutons de l'écran de pause
            screen.blit(background_main_title2, (title2_x, 0))
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                run = False
        # Vérifier si le menu des options est ouvert
        elif menu_state == "options":
            # Dessiner les différents boutons d'options
            screen.blit(background_main_title2, (title2_x, 0))
            if video_button.draw(screen):
                print("Paramètres vidéo")
            if audio_button.draw(screen):
                print("Paramètres audio")
            if keys_button.draw(screen):
                print("Changer les liaisons de touches")
            if back_button.draw(screen):
                menu_state = "main"
                show_title1 = True  # Afficher à nouveau le titre 1 lors du retour au menu principal
    else:
        # Afficher le texte centré
        text_surface = font.render("Click SPACE to start", True, TEXT_COL)
        text_rect = text_surface.get_rect()

        # Centrer le texte verticalement
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Afficher le texte centré
        screen.blit(text_surface, text_rect.topleft)
        screen.blit(background_main_title, (title_x, 0))

    # Gestionnaire d'événements
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = True
                show_title1 = not show_title1  # Inverser l'état de l'affichage du titre 1
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
