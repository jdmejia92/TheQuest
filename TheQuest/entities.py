import pygame as pg

class Ship(pg.sprite.Sprite):
    def __init__(self, screen, centrox, centroy):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("resources/images/StarShip/StarShip.png")
        self.rect = self.image.get_rect(centerx = centrox, centery = centroy)
        self.speedy = 5
        self.max_speed = 7

    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            self.rect.y -= self.speedy
        if key[pg.K_DOWN]:
            self.rect.y += self.speedy

        key_fast = pg.key.get_pressed()
        if key_fast[pg.K_LSHIFT] and key[pg.K_UP]:
           self.rect.y -= self.max_speed
        if key_fast[pg.K_LSHIFT] and key[pg.K_DOWN]:
            self.rect.y += self.max_speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()

class Meteor(pg.sprite.Sprite):
    def __init__(self, centrox, centroy):
        super().__init__()
        self.vx = 4
        self.x_ini = centrox
        self.y_ini = centroy
        self.image = pg.image.load("resources/images/Meteor/Meteor_ready.png")
        self.rect = self.image.get_rect(center=(centrox, centroy))

    def update(self):
        self.rect.x -= self.vx

    def pass_meteor(self):
        if self.rect.centerx == -10:
            return True

        return False 
