from doctest import ELLIPSIS_MARKER
from email.mime import image
from multiprocessing import set_forkserver_preload
from telnetlib import STATUS
import pygame as pg
from enum import Enum
import os

white = (255, 255, 255)

class ShipStatus(Enum):
    travel = 1
    arrive = 2
    lunch = 3
    explode = 4
    landing = 5


class Ship(pg.sprite.Sprite):
    def __init__(self, screen, cent_x, cent_y):
        super().__init__()
        self.screen = screen
        self.cent_x = cent_x
        self.cent_y = cent_y
        self.image_ship = pg.image.load("resources/images/StarShip/StarShip.png")
        self.image = self.image_ship
        self.rect = self.image.get_rect(centerx = self.cent_x, centery = self.cent_y)
        self.ini_speedy = 5
        self.speedy = self.ini_speedy
        self.max_speed = 5
        self.arrive_speed = 2
        self.rotation = 0
        self.angle = 0
        self.landing = 0
        self.ship_status = ShipStatus.travel

    def update(self):
        """if self.ship_status == ShipStatus.lunch:"""


        if self.ship_status == ShipStatus.arrive:
            if self.rect.centery >= self.screen.get_height()//2:
                self.rect.centery -= self.arrive_speed
                if self.rect.centery <= self.screen.get_height()//2:
                    self.arrive_speed = 0
            elif self.rect.centery <= self.screen.get_height()//2:
                self.rect.centery += self.arrive_speed
                if self.rect.centery >= self.screen.get_height()//2:
                    self.arrive_speed = 0
            
            if self.arrive_speed == 0:
                if self.rotation <= 180:
                    self.image = pg.transform.rotate(self.image_ship, self.angle)
                    self.angle += 1 % 180
                    self.rect = self.image.get_rect(center=self.rect.center)

                self.rotation += 1
                self.image_rotate = self.image
                self.width = self.image.get_rect().width
                self.height = self.image.get_rect().height

        elif self.ship_status == ShipStatus.landing:
            if self.rotation >= 180 and self.rect.right < self.screen.get_width():
                self.arrive_speed = 2
                self.rect.centerx += self.arrive_speed
                if self.rect.right >= self.screen.get_width():
                    self.arrive_speed = 0

            if self.rect.centerx >= self.screen.get_width() - 700:
                if self.rect.centerx % 10 == 0:
                    if self.landing <= 50:
                        self.image = pg.transform.scale(self.image_rotate, (self.width, self.height))
                        self.rect = self.image.get_rect(center=self.rect.center)
                        self.width -= 2.5
                        self.height -= 1
                    
                    self.landing += 1
               

        elif self.ship_status == ShipStatus.travel:               
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

    def reset(self):
        self.ship_status = ShipStatus.travel
        self.speedy = self.ini_speedy
        self.arrive_speed = 2
        self.image = self.image_ship
        self.rect.centerx = self.cent_x
        self.angle = 0
        self.rotation = 0
        self.landing = 0

        
        
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
    def __init__(self, screen, cent_x, cent_y):
        super().__init__()
        self.screen = screen
        self.centrox = cent_x
        self.x_ini = self.centrox
        self.y_ini = cent_y
        self.image = pg.image.load(os.path.join("resources/images/Arrive_World/New_World.png")).convert_alpha()
        self.rect = self.image.get_rect(centerx = self.x_ini, centery = self.y_ini)
        self.ini_vx = 5
        self.vx = self.ini_vx
        self.status_arrive = False

    def update(self):
        if self.status_arrive == True:
            self.rect.centerx -= self.vx
            if self.rect.centerx <= self.screen.get_width() + 450:
                self.vx = 0

    def reset(self):
        self.rect.centerx = self.centrox
        self.vx = self.ini_vx


    

