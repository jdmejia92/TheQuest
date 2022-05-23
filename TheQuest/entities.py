import pygame as pg
from TheQuest import FPS
from enum import Enum
import os
import sqlite3


white = (255, 255, 255)

#Base de datos
class ProcessData():
    def __init__(self):
        self.con = sqlite3.connect("data/Records.db")
        self.cur = self.con.cursor()

    #Mostrando los puntos en la pantalla final
    def show_records(self):
        self.cur.execute("""SELECT Iniciales, Puntaje FROM Records ORDER BY Puntaje DESC LIMIT 5""")
        n = self.cur.fetchall()
        return n

    #Para cargar el escensario dependiendo de si ganaste o perdiste
    def show_life(self):
        self.cur.execute("""SELECT Vidas FROM Records ORDER BY id DESC LIMIT 1""")
        n = self.cur.fetchone()[0]
        return int(n)

    #Comparar el puntaje visible mas bajo
    def lower_visible_point(self):
        self.cur.execute("""SELECT Puntaje FROM Records ORDER BY Puntaje DESC LIMIT 5""")
        n = self.cur.fetchall()[4][0]
        return n

    #Selecciona el ultimo id generado
    def show_lastid(self):
        self.cur.execute("""SELECT id FROM Records ORDER BY id DESC LIMIT 1""")
        n = self.cur.fetchone()[0]
        return int(n)

    #Muestra el puntaje obtenido en la partida
    def show_points(self):
        self.cur.execute("""SELECT Puntaje FROM Records ORDER BY id DESC LIMIT 1""")
        n = self.cur.fetchone()[0]
        return n

    #Compara e ultimo ID con el 5to de la lista de records
    def checkID(self):
        self.cur.execute("""SELECT id FROM Records ORDER BY id DESC LIMIT 1""")
        n = self.cur.fetchone()[0]
        try:
            self.cur.execute("""SELECT id, Puntaje FROM Records ORDER BY Puntaje DESC LIMIT 5""")
            m = self.cur.fetchall()[4][0]
        except IndexError:
            m = 0
        y = (n==m)
        return y

    #Muestra el puntaje mas bajo de los primeros 5
    def lower_visible_point(self):
        try:
            self.cur.execute("""SELECT Puntaje FROM Records ORDER BY Puntaje DESC LIMIT 5""")
            n = self.cur.fetchall()[4][0]
            return n
        except IndexError:
            return 0

    #Guarde la cantidad de puntos y vidas de la partida
    def player_record(self, life, points):
        self.con = sqlite3.connect("data/Records.db")
        self.cur = self.con.cursor()

        self.cur.execute(f"""INSERT INTO Records (Puntaje, Vidas) VALUES ('{points}', '{life}')""")

        self.con.commit()

    #En caso supere alguno de los mejores puntajes, guarda y actualiza las iniciales en la base de datos
    def update(self, id, initials):
        self.cur.execute(f"""UPDATE Records Set Iniciales = '{initials}' WHERE id = {id}""")

        self.con.commit()

    #En caso la base de datos se haya dañado
    def createdata(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Records (id INTEGER PRIMARY KEY AUTOINCREMENT, Iniciales TEXT, Puntaje INTEGER, Vidas INTEGER)""")
        
        self.con.commit()

    #Para borrar el puntaje en caso no haya superado el 5to mas bajo
    def deleteLowPoints(self, id):
        records = self.show_records()
        if len(records) >= 4:
            self.cur.execute(f"""DELETE FROM Records WHERE id LIKE '%{id}%'""")

        self.con.commit()

#Multiples estados de la nave
class ShipStatus(Enum):
    travel = 1
    arrive = 2
    lunch = 3
    explode = 4
    landing = 5
    takeoff = 6
    deploy = 7
    destroy = 8

#Nave
class Ship(pg.sprite.Sprite):
    def __init__(self, screen, cent_x, cent_y):
        super().__init__()
        self.screen = screen
        self.cent_x = cent_x
        self.cent_y = cent_y
        self.image_ship = pg.image.load("resources/images/StarShip/StarShip.png")
        self.image = self.image_ship
        self.rect = self.image.get_rect(centerx = self.cent_x, centery = self.cent_y)
        self.rect_image = self.rect
        self.ini_speedy = 5
        self.speedy = self.ini_speedy
        self.max_speed = 5
        self.arrive_speed = 2
        self.rotation = 0
        self.angle = 0
        self.landing = 0
        self.lunch = 0
        self.view = 0
        self.ship_status = ShipStatus.lunch

    def update(self):
        #Animacion cuando la nave llega al mundo
        if self.ship_status == ShipStatus.arrive:
            if self.rect.centery >= self.screen.get_height()//2:
                self.rect.centery -= self.arrive_speed
                if self.rect.centery <= self.screen.get_height()//2:
                    self.arrive_speed = 0
            elif self.rect.centery <= self.screen.get_height()//2:
                self.rect.centery += self.arrive_speed
                if self.rect.centery >= self.screen.get_height()//2:
                    self.arrive_speed = 0
            
            #Rotacion de la nave
            if self.arrive_speed == 0:
                if self.rotation <= 181:
                    self.image = pg.transform.rotate(self.image_ship, self.angle)
                    self.angle += 1
                    self.rect = self.image.get_rect(center=self.rect.center)

                self.rotation += 1
                self.image_rotate = self.image
                self.width = self.rect.width
                self.height = self.rect.height

        #La nave se pone mas pequena al acercarse al mundo
        elif self.ship_status == ShipStatus.landing:
            if self.rotation >= 181 and self.rect.right < self.screen.get_width():
                self.arrive_speed = 2
                self.rect.centerx += self.arrive_speed
                if self.rect.right >= self.screen.get_width():
                    self.arrive_speed = 0

            if self.rect.centerx >= self.screen.get_width() - 700:
                if self.rect.centerx % 10 == 0:
                    if self.landing <= 55:
                        self.image = pg.transform.smoothscale(self.image_rotate, (self.width, self.height))
                        self.rect = self.image.get_rect(center=self.rect.center)
                        self.width -= 2.5
                        self.height -= 1
                    
                    self.landing += 1

        #Cuando la nave se encuentra en movimiento
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

        #Cuando la nave arranca desde el mundo
        elif self.ship_status == ShipStatus.lunch:
            self.image = pg.transform.smoothscale(self.image_ship, (12.5, 5))
            self.rect = self.image.get_rect(x = 1, y = self.screen.get_height()//2)
            self.widthB = self.rect.w
            self.heightB = self.rect.h
            if self.view == 30:
                self.ship_status = ShipStatus.takeoff
            self.view += 1

            self.small_ship = self.image
            self.small_rect = self.rect

        #Sale del mundo
        elif self.ship_status == ShipStatus.takeoff:           
            if self.rect.centerx <= self.screen.get_width()//2:
                self.rect.centerx += 2
                if self.rect.centerx % 10 == 9 or self.rect.centerx % 10 == 5:
                    if self.lunch <= 55:
                        self.image = pg.transform.smoothscale(self.image_ship, (self.widthB, self.heightB))
                        self.rect = self.image.get_rect(center = self.rect.center)
                        self.widthB += 2.5
                        self.heightB += 1
                    self.lunch += 1
            elif self.rect.centerx >= self.screen.get_width()//2:
                self.ship_status = ShipStatus.deploy

        #Se coloca en posicion para empezar el juego
        elif self.ship_status == ShipStatus.deploy:
            self.rect.centerx -= 3
            if self.rect.centerx <= 80:
                self.ship_status = ShipStatus.travel   

        #Cuando la nave explota
        elif self.ship_status == ShipStatus.explode:
            self.kill()

    def reset(self):
        self.ship_status = ShipStatus.lunch
        self.speedy = self.ini_speedy
        self.arrive_speed = 2
        self.image = self.image_ship
        self.rect = self.rect_image
        self.rect.centery = self.cent_y
        self.angle = 0
        self.rotation = 0
        self.landing = 0
        self.view = 0
        self.lunch = 0

#Meteoros y Asteroides
class Meteor(pg.sprite.Sprite):
    def __init__(self, centrox, centroy, size):
        super().__init__()
        self.vx = 3
        self.vx_max = 4
        self.vx_big = 2
        self.vx_big_max = 3
        self.x_ini = centrox
        self.y_ini = centroy
        self.size = size
        if self.size == 1:
            self.image = pg.image.load(os.path.join("resources/images/Meteor/Meteor_ready.png")).convert_alpha()
            self.rect = self.image.get_rect(center=(self.x_ini, self.y_ini))
        elif self.size == 0:
           self.image = pg.image.load(os.path.join("resources/images/Meteor/Big_Meteor.png")).convert_alpha()
           self.rect = self.image.get_rect(center=(self.x_ini, self.y_ini))

    #Velocidad de los meteoros y asteroides
    def update(self):
            if self.size == 1:
                key = pg.key.get_pressed()
                if key[pg.K_RSHIFT]:
                    self.rect.x -= self.vx_max
                self.rect.x -= self.vx
            elif self.size == 0:
                key = pg.key.get_pressed()
                if key[pg.K_RSHIFT]:
                    self.rect.x -= self.vx_big_max
                self.rect.x -= self.vx_big

    def pass_meteor(self):
        if self.rect.centerx <= -50:
            return True

        return False 

class World(pg.sprite.Sprite):
    def __init__(self, screen, cent_x, cent_y, level):
        super().__init__()
        self.screen = screen
        self.centrox = cent_x
        self.x_ini = self.centrox
        self.y_ini = cent_y
        self.level = level
        if self.level == "Start":
            self.image = pg.image.load(os.path.join("resources/images/Worlds/Red_World.png")).convert_alpha()
            self.rect = self.image.get_rect(centerx = self.x_ini, centery = self.y_ini)
        elif self.level == "Midle":
            self.image = pg.image.load(os.path.join("resources/images/Worlds/Midle_World.png")).convert_alpha()
            self.rect = self.image.get_rect(centerx = self.x_ini, centery = self.y_ini)
        elif self.level == "Midle_lunch":
            self.image = pg.image.load(os.path.join("resources/images/Worlds/Midle_World.png")).convert_alpha()
            self.rect = self.image.get_rect(centerx = self.x_ini, centery = self.y_ini)
        elif self.level == "End":
            self.image = pg.image.load(os.path.join("resources/images/Worlds/New_World.png")).convert_alpha()
            self.rect = self.image.get_rect(centerx = self.x_ini, centery = self.y_ini)
        self.ini_vx = 3
        self.vx = self.ini_vx
        self.kill_count = 0
        self.status_arrive = False

    def update(self):
        if self.level == "Start" or self.level == "Midle_lunch":
            self.rect.centerx -= self.vx
            if self.rect.centerx <= -1400:
                self.vx = 0
                self.kill()

        elif self.level == "Midle" or self.level == "End":
            if self.status_arrive == True:
                self.rect.centerx -= self.vx
                if self.rect.centerx <= self.screen.get_width() + 450:
                    self.vx = 0

    def reset(self):
        self.rect.centerx = self.centrox
        self.vx = self.ini_vx

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.explosion_anim = {}
        self.explosion_anim['Big'] = []
        self.explosion_anim['Small'] = []
        self.explosion_anim['Ship'] = []
        #Cargar las explosiones pequeñas y grandes
        for i in range(71):
            explosion = pg.image.load(os.path.join(f"./resources/images/Explosion/ExplosionLarga/Explosion{i}.png")).convert_alpha()
            self.explosion_anim['Big'].append(explosion)
            small_explosion = pg.transform.scale(explosion, (60, 60))
            self.explosion_anim['Small'].append(small_explosion)
            ship_explosion = pg.transform.scale(explosion, (150, 150))
            self.explosion_anim['Ship'].append(ship_explosion)

        self.image = self.explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.active_explosion = 0
        self.animation_time = FPS
        self.current_time = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.current_time > self.animation_time:
            self.current_time = 0
            self.active_explosion += 1
            if self.active_explosion >= len(self.explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_anim[self.size][self.active_explosion]
                self.rect = self.image.get_rect()
                self.rect.center = center