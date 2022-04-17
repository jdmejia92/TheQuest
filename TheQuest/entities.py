from doctest import ELLIPSIS_MARKER
from email.mime import image
from telnetlib import STATUS
import pygame as pg
from enum import Enum

white = (255, 255, 255)

class ShipStatus(Enum):
    travel = 1
    arrive = 2
    lunch = 3
    explode = 4


class Ship(pg.sprite.Sprite):
    def __init__(self, screen, cent_x, cent_y):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("resources/images/StarShip/StarShip.png")
        self.rect = self.image.get_rect(centerx = cent_x, centery = cent_y)
        self.ini_speedy = 5
        self.speedy = self.ini_speedy
        self.max_speed = 5
        self.ship_travel = True
        self.ship_rotate = False
        self.rotate_time = 0
        self.current_time = 0
        self.angle = 0

    def update(self):
        if self.ship_travel == False:
            if self.rect.centery >= self.screen.get_height()//2:
                self.rect.centery -= self.speedy
                if self.rect.centery <= self.screen.get_height()//2:
                    self.speedy = 0
            elif self.rect.centery <= self.screen.get_height()//2:
                self.rect.centery += self.speedy
                if self.rect.centery >= self.screen.get_height()//2:
                    self.speedy = 0

        """if self.ship_rotate == True:
            print(self.angle)
            if self.angle == 0:
                self.image = self.image
                self.center = self.rect.center
            elif self.angle <= 1000:
                if self.angle % 100 == 0:
                    self.image = pg.transform.rotate(self.image, 18 * self.angle//100)
                    self.rect = self.image.get_rect(center=self.center)
            else:
                self.ship_rotate == False
                self.image = self.image
                self.angle = -1

            self.angle += 1"""
            
        if self.ship_travel == True:
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

    def arrive(self):
        self.ship_travel = False

    def reset(self):
        self.ship_travel = True
        self.ship_rotate = False
        self.speedy = self.ini_speedy
        
        
class Meteor(pg.sprite.Sprite):
    def __init__(self, centrox, centroy):
        super().__init__()
        self.vx = 3
        self.x_ini = centrox
        self.y_ini = centroy
        self.image = pg.image.load("resources/images/Meteor/Meteor_ready.png")
        self.rect = self.image.get_rect(center=(centrox, centroy))

    def update(self):
        self.rect.x -= self.vx

    def pass_meteor(self):
        if self.rect.centerx <= -30:
            return True

        return False 

class World(pg.sprite.Sprite):
    def __init__(self, screen, centrox, centroy, radio = 200):
        super().__init__()
        self.radio = radio
        self.screen = screen
        self.centrox = centrox
        self.x_ini = self.centrox
        self.y_ini = centroy

        self.image = pg.Surface((radio * 2, radio * 2), pg.SRCALPHA)
        pg.draw.circle(self.image, white, (self.x_ini, self.y_ini), self.radio)
        self.rect = self.image.get_rect(center=(self.x_ini, self.y_ini))
        
        self.ini_vx = 4
        self.vx = self.ini_vx
        self.status_arrive = False      

    def arrive(self):
        self.status_arrive = True

    def draw(self):
        pg.draw.circle(self.screen, white, (self.x_ini, self.y_ini), self.radio)

    def update(self):
        if self.status_arrive == True:
            self.x_ini -= self.vx
            if self.x_ini <= self.screen.get_width():
                self.vx = 0

    def reset(self):
        self.x_ini = self.centrox
        self.vx = self.ini_vx


    

