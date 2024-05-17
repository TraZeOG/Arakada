
def arakada2_main():
    import pygame
    import random
    import pickle

    pygame.init()
    pygame.display.set_caption("Arakada 2")
    clock = pygame.time.Clock()
    fps = 60
    screen_height = 1000
    screen_width = 1000
    screen= pygame.display.set_mode((screen_width, screen_height))


    clr_wheat = (179,202,245)
    clr_black = (0,0,0)
    clr_white = (255,255,255)
    clr_play = (235,212,169)
    font_bauhaus_50 = pygame.font.SysFont("Bauhaus 93", 50)
    font_bauhaus_30 = pygame.font.SysFont("Bauhaus 93", 30)
    font_lilitaone_70 = pygame.font.Font("games/Arakada2/fonts/LilitaOne-Regular.ttf", 80)
    img_coeur_on = pygame.image.load("games/Arakada2/sprites/img_coeur_on.webp")
    img_coeur_off = pygame.image.load("games/Arakada2/sprites/img_coeur_off.webp")
    img_background_play = pygame.image.load("games/Arakada2/sprites/img_background_play.webp")
    img_background_summary = pygame.image.load("games/Arakada2/sprites/img_background_summary.webp")
    img_meteorite = pygame.image.load("games/Arakada2/sprites/img_meteorite_menu.webp")
    img_joueur = pygame.image.load("games/Arakada2/sprites/img_citron_menu.webp")

    frequency = 40
    game_over = 0
    vies = 3
    menu_principal = True
    timer = 0
    counter = 0
    score = 0
    pickle_in = open(f'games/Arakada2/data/data_main', 'rb')
    high_score = pickle.load(pickle_in)
    types = ["gros", "speed", "zigzag", "normal"]

    def draw_text(texte, font, couleur, x, y):
        img = font.render(texte, True, couleur)
        screen.blit(img, (x, y))

    def reset_level():
        grp_object.empty()
        vies = 3
        score = 0
        frequency = 40
        timer = 0
        player.reset(screen_width // 2 - 35, screen_height // 2 - 35)
        game_over = 0

        return game_over, vies, timer, score, frequency

    def save():
        pickle_out = open('games/Arakada2/data/data_main', 'wb')
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


    bouton_exit = Bouton(screen_width - 105, 15, 90, 50, pygame.image.load("games/Arakada2/sprites/img_bouton_exit.webp"))
    bouton_start = Bouton(screen_width // 2 - 130, screen_height // 2 - 110, 260, 100, pygame.image.load("games/Arakada2/sprites/img_bouton_start.webp"))
    bouton_restart = Bouton(screen_width // 2 - 130, screen_height // 2 + 110, 260, 100, pygame.image.load("games/Arakada2/sprites/img_bouton_restart.webp"))
    bouton_menu = Bouton(screen_width // 2 - 130, screen_height // 2 + 240, 260, 100, pygame.image.load("games/Arakada2/sprites/img_bouton_menu.webp"))
    bouton_resume = Bouton(screen_width // 2 - 156, screen_height // 2 - 60, 312, 142, pygame.image.load("games/Arakada2/sprites/img_bouton_resume.webp"))


    class Object(pygame.sprite.Sprite):
        def __init__(self, type, cote, xx, yy):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("games/Arakada2/sprites/img_meteorite.webp")
            if type == "zigzag" or type == "speed":
                self.image = pygame.image.load("games/Arakada2/sprites/img_soucoupe.webp")
                self.image = pygame.transform.scale(self.image, (50,50))
                self.direction = 2
                self.counter = 0
            if type == "normal":
                self.image = pygame.transform.scale(self.image, (70,70))
            if type == "gros":
                self.image = pygame.transform.scale(self.image, (90,90))
            self.rect = self.image.get_rect()
            self.type = type
            if cote == 0:
                self.rect.x = screen_width
                if yy > 0:
                    self.rect.y = random.randint(30, screen_height * 2 // 3)
                elif yy < 0:
                    self.rect.y = random.randint(screen_height * 2 // 3, screen_height - 30)
                else:
                    self.rect.y = random.randint(30, screen_height - 30)
            if cote == 1:
                if xx > 0:
                    self.rect.x = random.randint(30, screen_width * 2 // 3)
                elif xx < 0:
                    self.rect.x = random.randint(screen_width * 2 // 3, screen_width - 30)
                else:
                    self.rect.x = random.randint(30, screen_width - 30)
                self.rect.y = -100
            if cote == 2:
                self.rect.x = -100
                if yy > 0:
                    self.rect.y = random.randint(30, screen_height * 2 // 3)
                elif yy < 0:
                    self.rect.y = random.randint(screen_height * 2 // 3, screen_height - 30)
                else:
                    self.rect.y = random.randint(30, screen_height - 30)
            if cote == 3:
                if xx > 0:
                    self.rect.x = random.randint(30, screen_width * 2 // 3)
                elif xx < 0:
                    self.rect.x = random.randint(screen_width * 2 // 3, screen_width - 30)
                else:
                    self.rect.x = random.randint(30, screen_width - 30)
                self.rect.y = screen_height
            vitesse = xx + yy
            if vitesse <= 5:
                if xx < yy:
                    xx += 1
                else:
                    yy += 1
            self.dx = xx
            self.dy = yy

        def update(self):
            self.rect.x += self.dx 
            self.rect.y += self.dy
            if self.type == "zigzag":
                self.counter += 1
                if self.counter == 60:
                    self.direction *= -1
                    self.counter = 0
                self.rect.x += self.direction
                self.rect.y -= self.direction
            if self.type == "speed":
                self.rect.x += 1
                self.rect.y += 1
            if self.type == "default":
                self.rect.y += 2
            if self.type == "gros":
                self.rect.y -= 1
                self.rect.x -= 1
                

    grp_object = pygame.sprite.Group()


    class Joueur():
        def __init__(self, x, y):
            self.reset(x, y)

        def update(self, game_over, vies):
            dx = 0
            dy = 0
            if game_over == 0:

                max_speed_x = 12 + timer // 30
                max_speed_y = 12 + timer // 30
                acceleration = max_speed_x // 2
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

                if key[pygame.K_UP]:
                    if not self.vitesse_y <= -1 * max_speed_y:
                        self.vitesse_y -= acceleration
                    else:
                        self.vitesse_y = - 1 * max_speed_y
                if key[pygame.K_DOWN]:
                    if not self.vitesse_y >= max_speed_y:
                        self.vitesse_y += acceleration
                    else:
                        self.vitesse_y = max_speed_y
                if not key[pygame.K_UP] and not key[pygame.K_DOWN]:
                    if self.vitesse_y > 1:
                        self.vitesse_y -= freinage
                        if self.vitesse_y > 7:
                            self.vitesse_y = 7
                    elif self.vitesse_y < -1:
                        self.vitesse_y += freinage
                        if self.vitesse_y < -7:
                            self.vitesse_y = -7
                    else:
                        self.vitesse_y = 0
                dy += int(self.vitesse_y)
                            
                self.rect.x += dx
                self.rect.y += dy

                if player.rect.left < 0:
                    player.rect.left = 0
                    self.vitesse_x = 0
                if player.rect.right > screen_width:
                    player.rect.right = screen_width
                    self.vitesse_x = 0
                if player.rect.top < 0:
                    player.rect.top = 0
                    self.vitesse_y = 0
                if player.rect.bottom > screen_width:
                    player.rect.bottom = screen_width
                    self.vitesse_y = 0


                if vies == 0:
                    game_over = -1
                if pygame.sprite.spritecollide(self, grp_object, True):
                    vies -= 1

            if game_over == 0:
                screen.blit(self.image, self.rect)
            
            return game_over, vies

        def reset(self, x, y):

            self.image = pygame.image.load(f"games/Arakada2/sprites/img_citron.webp")
            self.image = pygame.transform.scale(self.image, (35,35))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.vitesse_y = 0
            self.vitesse_x = 0

    player = Joueur(95, screen_height - 140)


    run=True
    while run:

        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                save()
                run = False

        clock.tick(fps)
        if menu_principal == True:
            screen.fill(clr_wheat)
            draw_text("Arakada n°2", font_lilitaone_70, clr_black, screen_width // 2 - 210, screen_height // 2 - 230)
            draw_text("Jeu du vaisseau", font_lilitaone_70, clr_black, screen_width // 2 - 260, screen_height // 2 + 30)
            screen.blit(img_meteorite, (screen_width // 2 + 25, screen_height // 2 + 190))
            screen.blit(img_joueur, (screen_width // 2 - 175, screen_height // 2 + 190))
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
                    score += 1
                    counter = 0
                    if timer % 5 == 0:
                        frequency -= 1

                screen.blit(img_background_play, (0,0))
                if 0 <= timer % 60 < 10:
                    draw_text(f"0{timer // 60}:0{timer % 60}", font_bauhaus_50, clr_white, 10, 20)
                else:
                    draw_text(f"0{timer // 60}:{timer % 60}", font_bauhaus_50, clr_white, 10, 20)
                draw_text(f"Fréquence: {40 - frequency}", font_bauhaus_30, clr_white, screen_width - 196, screen_height - 40)
                draw_text(f"Vitesse: {1 + timer // 20}", font_bauhaus_30, clr_white, screen_width - 148, screen_height - 70)

                n = random.randint(0, frequency)
                if n == 1:
                    if frequency > 25:
                        frequency -= 1
                    type = random.randint(0, len(types) - 1)
                    cote = random.randint(0,3)
                    x = random.randint(1 + timer // 20, 5 + timer // 20)
                    y = random.randint(1 + timer // 20, 5 + timer // 20)
                    if x == 0:
                        y *= 2
                    if y == 0:
                        x *= 2
                    if cote == 0:
                        x *= -1
                    if cote == 3:
                        y *= -1
                    obj = Object(types[type], cote, x, y)
                    grp_object.add(obj)

                grp_object.update()
                grp_object.draw(screen)
                for i in range(vies):
                    screen.blit(img_coeur_on, (screen_width - 260 + 80 * i, 7))
                for i in range(3 - vies):
                    screen.blit(img_coeur_off, (screen_width - 100 - 80 * i, 7))
                game_over, vies = player.update(game_over, vies)


            if game_over == -1:
                if score > high_score:
                    high_score = score
                screen.blit(img_background_summary, (screen_width // 2 - 257, screen_height // 2 - 320))
                if bouton_restart.draw():
                    game_over = 1
                if bouton_menu.draw():
                    menu_principal = True
                draw_text("Summary :", font_lilitaone_70, clr_black, screen_width // 2 - 180, screen_height // 2 - 250)
                draw_text(f"Score: {score}", font_bauhaus_50, clr_black, screen_width // 2 - 100, screen_height // 2 - 110)
                if 0 < timer % 60 < 10:
                    draw_text(f"Timer: 0{timer // 60}:0{timer % 60}", font_bauhaus_50, clr_black, screen_width // 2 - 140, screen_height // 2 + 10)
                else:
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
