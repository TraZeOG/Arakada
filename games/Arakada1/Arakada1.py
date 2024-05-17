
def arakada1_main():
    import pygame
    import random
    import pickle

    pygame.init()
    pygame.display.set_caption("Arakada 1")
    clock = pygame.time.Clock()
    fps = 60
    screen_height = pygame.display.Info().current_h - 100
    screen_width = screen_height * 2 // 3
    screen= pygame.display.set_mode((screen_width, screen_height))
    clr_wheat = (179,202,245)
    clr_black = (0,0,0)
    clr_play = (235,212,169)
    game_over = 0
    n = 0
    frequency = 120
    fr11 = 10
    fr12 = 11
    fr2 = 20
    score = 0
    vies = 3
    menu_principal = True
    counter = 0
    types = ["normal", "gros", "zigzag", "speed"]
    timer = 0
    pickle_in = open(f'games/Arakada1/data/data_main', 'rb')
    high_score = pickle.load(pickle_in)


    img_background_score = pygame.image.load("games/Arakada1/sprites/img_background_score.webp")
    img_background_play = pygame.image.load("games/Arakada1/sprites/img_background_play.webp")
    img_coeur_on = pygame.image.load("games/Arakada1/sprites/img_coeur_on.webp")
    img_background_area = pygame.image.load("games/Arakada1/sprites/img_background_area.webp")
    img_background_area = pygame.transform.scale(img_background_area, (screen_width, 2))
    img_joueur = pygame.image.load("games/Arakada1/sprites/img_joueur.webp")
    img_citron= pygame.image.load("games/Arakada1/sprites/img_citron.webp")

    img_coeur_off = pygame.image.load("games/Arakada1/sprites/img_coeur_off.webp")
    font_bauhaus_50 = pygame.font.SysFont("Bauhaus 93", 50)
    font_bauhaus_30 = pygame.font.SysFont("Bauhaus 93", 30)
    font_lilitaone_70 = pygame.font.Font("games/Arakada1/fonts/LilitaOne-Regular.ttf", 80)

    def draw_text(texte, font, couleur, x, y):
        img = font.render(texte, True, couleur)
        screen.blit(img, (x, y))

    def reset_level():
        grp_amis.empty()
        grp_ennemis.empty()
        vies = 3
        score = 0
        frequency = 120
        timer = 0
        player.reset(screen_width // 2, screen_height - 140)
        game_over = 0

        return game_over, vies, timer, score, frequency

    def save():
        pickle_out = open('games/Arakada1/data/data_main', 'wb')
        pickle.dump(high_score, pickle_out)
        pickle_out.close()

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


    bouton_exit = Bouton(screen_width - 105, 15, 90, 50, pygame.image.load("games/Arakada1/sprites/img_bouton_exit.webp"))
    bouton_start = Bouton(screen_width // 2 - 130, screen_height // 2 - 110, 260, 100, pygame.image.load("games/Arakada1/sprites/img_bouton_start.webp"))
    bouton_restart = Bouton(screen_width // 2 - 130, screen_height // 2 + 110, 260, 100, pygame.image.load("games/Arakada1/sprites/img_bouton_restart.webp"))
    bouton_menu = Bouton(screen_width // 2 - 130, screen_height // 2 + 240, 260, 100, pygame.image.load("games/Arakada1/sprites/img_bouton_menu.webp"))
    bouton_resume = Bouton(screen_width // 2 - 156, screen_height // 2 - 60, 312, 142, pygame.image.load("games/Arakada1/sprites/img_bouton_resume.webp"))

    class Object(pygame.sprite.Sprite):
        def __init__(self, groupe, type):
            pygame.sprite.Sprite.__init__(self)
            self.type = type
            if groupe == "ennemi":
                self.image = pygame.image.load(f"games/Arakada1/sprites/\img_bombe.webp")
            if groupe == "friendly":
                self.image = pygame.image.load(f"games/Arakada1/sprites/\img_friendly.webp")
            if type == "zigzag":
                self.image = pygame.image.load(f"games/Arakada1/sprites/\img_cerise.webp")
                self.image = pygame.transform.scale(self.image, (50,50))
                self.counter = 0
                self.direction = 2
            if type == "normal" or type == "speed":
                self.image = pygame.image.load(f"games/Arakada1/sprites/\img_citron.webp")
                self.image = pygame.transform.scale(self.image, (70,70))
            if type == "gros":
                self.image = pygame.image.load(f"games/Arakada1/sprites/\img_ananas.webp")
                self.image = pygame.transform.scale(self.image, (90,90))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(10, screen_width - 90)
            self.rect.y = 0

        def update(self):
            self.rect.y += 1 + timer // 10
            if self.type == "zigzag":
                self.counter += 1
                if self.counter == 60:
                    self.direction *= -1
                    self.counter = 0
                self.rect.x += self.direction
            if self.type == "speed":
                self.rect.y += 1
            if self.type == "default":
                self.rect.y += 2
            if self.type == "gros":
                self.rect.y -= 1
                

    grp_amis = pygame.sprite.Group()
    grp_ennemis = pygame.sprite.Group()

    class Joueur():

        def __init__(self, x, y):
            self.reset(x, y)

        def update(self, game_over, score, vies):
            dx = 0
            max_speed_x = 12 + timer // 30
            acceleration = 2
            freinage = 4
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                if not self.vitesse_x <= -1 * max_speed_x:
                    self.vitesse_x -= acceleration
                else:
                    self.vitesse_x = - 1 * max_speed_x
            if key[pygame.K_RIGHT]:
                if not self.vitesse_x >= max_speed_x:
                    self.vitesse_x += acceleration
                else:
                    self.vitesse_x = max_speed_x
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                if self.vitesse_x > 1:
                    self.vitesse_x -= freinage
                    if self.vitesse_x > 7:
                        self.vitesse_x = 7
                elif self.vitesse_x < -1:
                    self.vitesse_x += freinage
                    if self.vitesse_x < -7:
                        self.vitesse_x = -7
                else:
                    self.vitesse_x = 0
            dx += int(self.vitesse_x)
            self.rect.x += dx
            if player.rect.left < 0:
                player.rect.left = 0
                self.vitesse_x = 0
            if player.rect.right > screen_width:
                player.rect.right = screen_width
                self.vitesse_x = 0


            
            if vies == 0:
                game_over = -1
            if pygame.sprite.spritecollide(self, grp_amis, True):
                score += 1
            if pygame.sprite.spritecollide(self, grp_ennemis, True):
                vies -= 1

            if game_over == 0:
                screen.blit(self.image, self.rect)

            return game_over, score, vies
        
        def reset(self, x, y):
            self.image = pygame.image.load(f"games/Arakada1/sprites/\img_joueur.webp")
            self.image = pygame.transform.scale(self.image, (60,20))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vitesse_y = 0
            self.vitesse_x = 0
            self.en_saut = False
            self.airtime = False
            self.vitesse_fin_y = 0
            self.images_right = []
            self.images_left = []
            self.index = 0
            self.counter = 0
            self.direction = 1
    player = Joueur(screen_width // 2, screen_height - 140)

    run=True
    while run:

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                save()
                run = False

        clock.tick(fps)
        if menu_principal == True:
            screen.fill(clr_wheat)
            draw_text("Arakada n°1", font_lilitaone_70, clr_black, screen_width // 2 - 210, screen_height // 2 - 230)
            draw_text("Jeu du fruit", font_lilitaone_70, clr_black, screen_width // 2 - 190, screen_height // 2 + 30)
            screen.blit(img_citron, (screen_width // 2 - 35, screen_height // 2 + 190))
            screen.blit(img_joueur, (screen_width // 2 - 90, screen_height // 2 + 300))
            if bouton_start.draw():
                menu_principal = False
                game_over = 1
            if bouton_exit.draw():
                save()
                run = False
        else:
            if game_over == 0:
                counter += 1
                if counter == 60:
                    timer += 1
                    counter = 0

                key = pygame.key.get_pressed()
                if key[pygame.K_o]:
                    vies -= 1
                if key[pygame.K_p]:
                    score += 5
                    timer += 5
                screen.fill(clr_play)
                screen.blit(img_background_area, (0, screen_height - 132))
                grp_amis.update()
                grp_ennemis.update()
                grp_amis.draw(screen)
                grp_ennemis.draw(screen)
                screen.blit(img_background_score, (0,0))
                draw_text(f"Score: {score}", font_bauhaus_50, clr_black, screen_width // 2 - 160, 20)
                draw_text(f"0{timer // 60}:{timer % 60}", font_bauhaus_50, clr_black, 10, 20)
                draw_text(f"Vitesse: {1 + timer // 10}", font_bauhaus_30, clr_black, screen_width - 150, screen_height - 40)
                for i in range(vies):
                    screen.blit(img_coeur_on, (screen_width // 2 + 70 + 80 * i, 7))
                for i in range(3 - vies):
                    screen.blit(img_coeur_off, (screen_width // 2 + 230 - 80 * i, 7))
                game_over, score, vies = player.update(game_over, score, vies)

                n = random.randint(0, frequency)
                if n == fr11 or n == fr12:
                    index = random.randint(0,len(types) - 1)
                    object = Object("friendly", types[index])
                    grp_amis.add(object) 
                if n == fr2:
                    object = Object("ennemi", "default")
                    grp_ennemis.add(object)  
                    if frequency > 27:
                        frequency -= 1 

                if key[pygame.K_ESCAPE]:
                    game_over = 2
                    screen.blit(img_background_play, (screen_width // 2 - 257, screen_height // 2 - 320))
                    draw_text("Pause", font_lilitaone_70, clr_black, screen_width // 2 - 100, screen_height // 2 - 180)
            if game_over == -1:
                if score > high_score:
                    high_score = score
                screen.blit(img_background_play, (screen_width // 2 - 257, screen_height // 2 - 320))
                if bouton_restart.draw():
                    game_over = 1
                if bouton_menu.draw():
                    menu_principal = True
                draw_text("Summary :", font_lilitaone_70, clr_black, screen_width // 2 - 180, screen_height // 2 - 250)
                draw_text(f"Score: {score}", font_bauhaus_50, clr_black, screen_width // 2 - 100, screen_height // 2 - 110)
                draw_text(f"Timer: 0{timer // 60}:{timer % 60}", font_bauhaus_50, clr_black, screen_width // 2 - 140, screen_height // 2 + 10)
                draw_text(f"Meilleur score: {high_score}", font_bauhaus_50, clr_black, screen_width // 2 - 200, screen_height // 2 - 50)

            if game_over == 1:
                game_over, vies, timer, score, frequency = reset_level()

            if game_over == 2:
                if bouton_resume.draw():
                    game_over = 0
                if bouton_menu.draw():
                    menu_principal = True
            

        pygame.display.update()
