import pygame

class ButtonText:
    def __init__(self, x, y, text, font, text_col, scale):
        font_size = int(font.get_height() * scale)
        font_a = "assets/buttons/TrajanPro-Regular.ttf"
        self.font = pygame.font.Font(font_a, font_size)
        self.text_col = text_col
        self.clicked = False

        # Créer une surface du texte
        self.text_surface = self.font.render(text, True, text_col)
        self.rect = self.text_surface.get_rect(topleft=(x, y))

    def draw(self, surface):
        action = False

        # Obtenir la position de la souris
        pos = pygame.mouse.get_pos()

        # Vérifier si la souris est sur le texte
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        elif pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Afficher le texte sur la surface
        surface.blit(self.text_surface, self.rect.topleft)

        return action
