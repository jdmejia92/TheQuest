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
    def __init__(self, screen, centrox, centroy):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("resources/images/StarShip/StarShip.png")
        self.rect = self.image.get_rect(centerx = centrox, centery = centroy)
        self.speedy = 5
        self.max_speed = 7
        self.ship_travel = True
        self.ship_rotate = False
        self.rotate_time = 0
        self.current_time = 0
        self.angel = 0

    def update(self):
        if self.ship_rotate == True:
            if self.rect.centery >= self.screen.get_height()//2:
                self.rect.centery -= self.speedy
                if self.rect.centery == self.screen.get_height()//2:
                    self.speedy = 0
            elif self.rect.centery <= self.screen.get_height()//2:
                self.rect.centery += self.speedy
                if self.rect.centery == self.screen.get_height()//2:
                    self.speedy = 0
            else:
                self.speedy = 0
      

            """self.rect.y = self.screen.get_height()//2
            self.angel = 0
            if self.angel >= 180:
                self.image = pg.transform.rotate(self.image, self.angel)
            
            self.angel += 1"""
            
        else:

            """if self.rotate_time == 0:
                self.image = self.image
                self.centro = self.rect.center
            elif self.rotate_time <= 1000:
                if self.rotate_time % 100 == 0:
                    self.image = pg.transform.rotate(self.image, (18 * self.rotate_time // 100))
                    self.rect = self.image.get_rect(center = self.centro)
            else:
                self.ship_rotate = False
                self.rotate_time = -1"""
        
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
        
        self.vx = 1
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
        self.vx = 1


    

