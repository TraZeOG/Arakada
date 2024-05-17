import pygame
import pickle
from games.Arakada1.Arakada1 import arakada1_main
from games.Arakada2.Arakada2 import arakada2_main



pygame.init()
pygame.display.set_caption("Arakada")
clock = pygame.time.Clock()
fps = 60
screen_height = pygame.display.Info().current_h - 100
screen_width = screen_height * 3 // 2
screen= pygame.display.set_mode((screen_width, screen_height))
clr_wheat = (149,212,175)
clr_black = (0,0,0)
clr_play = (235,212,169)
menu_principal = True

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

bouton_exit = Bouton(screen_width - 105, 15, 90, 50, pygame.image.load("sprites/img_bouton_exit.webp"))
bouton_start = Bouton(screen_width // 2 - 130, screen_height // 2 - 110, 260, 100, pygame.image.load("sprites/img_bouton_start.webp"))
bouton_restart = Bouton(screen_width // 2 - 130, screen_height // 2 + 110, 260, 100, pygame.image.load("sprites/img_bouton_restart.webp"))
bouton_menu = Bouton(screen_width // 2 - 130, screen_height // 2 + 240, 260, 100, pygame.image.load("sprites/img_bouton_menu.webp"))
bouton_resume = Bouton(screen_width // 2 - 156, screen_height // 2 - 60, 312, 142, pygame.image.load("sprites/img_bouton_resume.webp"))

run=True
while run:

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run = False

    clock.tick(fps)

    if menu_principal == True:
        screen.fill(clr_wheat)
        if bouton_exit.draw():
            run = False
        if bouton_start.draw():
            arakada1_main()
            screen= pygame.display.set_mode((screen_width, screen_height))
        if bouton_restart.draw():
            arakada2_main()
            screen= pygame.display.set_mode((screen_width, screen_height))

    pygame.display.update()

pygame.quit()