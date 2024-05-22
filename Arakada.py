import pygame
import pickle
from games.Arakada1.Arakada1 import arakada1_main
from games.Arakada2.Arakada2 import arakada2_main



pygame.init()
pygame.display.set_caption("Arakada")
clock = pygame.time.Clock()
fps = 60
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen_size = (screen_width, screen_height) 
screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clr_wheat = (149,212,175)
clr_black = (0,0,0)
clr_white = (255,255,255)
clr_play = (235,212,169)
font_lilitaone_80 = pygame.font.Font("games/Arakada1/fonts/LilitaOne-Regular.ttf", 100)
font_lilitaone_50 = pygame.font.Font("games/Arakada1/fonts/LilitaOne-Regular.ttf", 50)
menu_principal = True
menu_games = False

class Bouton():

    def __init__(self, x, y, width, height, image):
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        reset_click = False
        mouse_cos = pygame.mouse.get_pos()
        screen.blit(self.image, self.rect)
        if self.rect.collidepoint(mouse_cos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                reset_click = True
                self.clicked = False
        return reset_click


def draw_text(texte, font, couleur, x, y):
    img = font.render(texte, True, couleur)
    text_width, text_height = font.size(texte)
    screen.blit(img, (x - text_width // 2, y - text_height // 2))


bouton_exit = Bouton(screen_width - 105, 15, 90, 50, pygame.image.load("sprites/img_bouton_exit.webp"))
bouton_play1 = Bouton(screen_width // 2 - 270 - 260, screen_height // 2 + 60, 260, 100, pygame.image.load("sprites/img_bouton_play.webp"))
bouton_play2 = Bouton(screen_width // 2 + 270, screen_height // 2 + 60, 260, 100, pygame.image.load("sprites/img_bouton_play.webp"))
bouton_start = Bouton(screen_width // 2 - 130, screen_height // 2 - 50, 260, 100, pygame.image.load("sprites/img_bouton_start.webp"))

run=True
while run:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run = False

    clock.tick(fps)

    if menu_principal:
        screen.blit(pygame.transform.scale(pygame.image.load("sprites/img_background_principal.jpg"), (screen_width, screen_height)), (0,0))

        if bouton_exit.draw():
            run = False
        if bouton_start.draw():
            menu_principal = False
            menu_games = True
        draw_text("Arakada games", font_lilitaone_80, clr_white, 420, screen_height // 2 - 320)


    if menu_games:
        screen.blit(pygame.transform.scale(pygame.image.load("sprites/img_background_game.jpg"), (screen_width, screen_height)), (0,0))

        draw_text("Arakada games", font_lilitaone_80, clr_black, screen_width // 2, screen_height // 2 - 280)
        draw_text("Arakada 1", font_lilitaone_50, clr_black, screen_width // 2 - 400, screen_height // 2 - 80)
        draw_text("Arakada 2", font_lilitaone_50, clr_black, screen_width // 2 + 400, screen_height // 2 - 80)

        if bouton_play1.draw():
            arakada1_main()
            screen= pygame.display.set_mode((screen_width, screen_height))

        if bouton_play2.draw():
            arakada2_main()
            screen= pygame.display.set_mode((screen_width, screen_height))

        if bouton_exit.draw():
            menu_games = False
            menu_principal = True

    pygame.display.update()

pygame.quit()