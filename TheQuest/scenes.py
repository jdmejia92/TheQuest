import pygame as pg
from TheQuest import FPS, levels
from TheQuest.entities import Meteor, Ship, World, ShipStatus
import os
import sqlite3

white = (255, 255, 255)

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font_press = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 20)
        self.clock = pg.time.Clock()
        self.delay = 1200
        self.current_time = pg.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.show = True

    #Texto que parpadee
    def press_continue(self, texto):
        if self.current_time >= self.change_time:
                self.change_time = self.current_time + self.delay
                self.show = not self.show

        if self.show:
            press_continue = self.font_press.render(f"{texto}", True, white)
            rectexto_press = press_continue.get_rect()
            self.screen.blit(press_continue, ((self.screen.get_width() - rectexto_press.width)//2,
                                            (self.screen.get_height() - rectexto_press.h) - 30))

    def bucle_ppal(self) -> bool:
        return

class Intro(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.cover = pg.image.load("./resources/images/Worlds/Earth_red.jpg")
        self.font_title = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 60)
        
       
    def bucle_ppal(self):
        while True:
            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    return False

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True

            self.screen.blit(self.cover, (0, 0))
            title = self.font_title.render("THE QUEST", True, white)
            rectexto = title.get_rect()

            self.screen.blit(title, ((self.screen.get_width() - rectexto.width)//2,
                                             (self.screen.get_height() - rectexto.h)//2))

            self.press_continue("Presiona ESPACIO para iniciar")
            
            pg.display.flip()

class History(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.historia = pg.image.load("./resources/images/Worlds/Earth_red.jpg")

    def bucle_ppal(self) -> bool:
        while True:

            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return True
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return pg.quit()
            
            self.current_time = pg.time.get_ticks()

            self.screen.blit(self.historia, (0, 0))

            self.press_continue("Presione ESPACIO para continuar")

            pg.display.flip()


class Play(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.font_counter = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 13)
        self.ship = Ship(self.screen, 80, self.screen.get_height()//2)
        self.world = World(self.screen, self.screen.get_width() + 1000, self.screen.get_height()//2)
        self.meteors = pg.sprite.Group()
        self.all = pg.sprite.Group()
        self.clock.tick(FPS)
        self.points = 0
        self.life_count = 3

        #Fondo cargado
        self.backgrounds = []
        self.active_background = 0
        self.how_many = 0
        self.animation_time = FPS

        self.load_background()

        self.current_time = 0

    #Carga del fondo movible
    def load_background(self):
        space = pg.image.load(os.path.join("./resources/images/Background/New_Background.png")).convert_alpha()
        for colum in range(1600):
            x = colum + 1

            image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
            image.blit(space, (0,0), (x, 0, self.screen.get_width(), self.screen.get_height()))

            self.backgrounds.append(image)

        self.how_many = len(self.backgrounds)
        self.background = self.backgrounds[self.active_background]

    #Moviemiento del fongo
    def background_change(self, dt):
        self.current_time += dt
        if self.ship.ship_status == ShipStatus.travel:
            if self.current_time > self.animation_time:
                self.current_time = 0
                self.active_background += 1
                if self.active_background >= len(self.backgrounds):
                    self.active_background = 0
                
                self.background = self.backgrounds[self.active_background]

    #Reinicio al pasar de nivel
    def reset(self):
        self.meteors.empty()
        self.all.empty()
        self.all.add(self.world, self.ship)
        self.points = 0

    #Creacion de meteoros
    def create_meteors(self, level):
        for col, fil in levels[level]:
            m = Meteor(800 * col, 30 * fil)
            self.meteors.add(m)
        self.all.add(self.meteors)  

    #Contadores en pantalla
    def counters(self, level):
        life_text = self.font_counter.render('Contador de vidas: ' + str(self.life_count), True, (255, 255, 255))
        level_text = self.font_counter.render('Level: ' + str(level + 1), True, (255, 255, 255))
        points = self.font_counter.render('Puntos: ' + str(self.points), True, (255, 255, 255))
        self.screen.blit(life_text, (10, 10))
        self.screen.blit(level_text, (10, 25))
        self.screen.blit(points, (10, 40))
    
    #Llenar la base de datos con el puntaje y vidas
    def write_records(self, points, name):
        con = sqlite3.connect("data/Records.db")

        cur = con.cursor()

        cur.execute("""
                SELECT *
                FROM Records
                ORDER BY Puntaje DESC
                LIMIT 5
                """)
        e = cur.fetchall()

        if len(e) == 5:
            if e[4][1] <= self.points:
                insert = f"""INSERT INTO Records VALUES ('{name}', '{points}')"""
                cur.executescript(insert)
        elif len(e) <= 5:
            insert = f"""INSERT INTO Records VALUES ('{name}', '{points}')"""
            cur.executescript(insert)

        con.commit()

        con.close()


    #Juego
    def bucle_ppal(self) -> bool:
        level = 0
        self.reset()
        self.life_count = 3
                
        while self.life_count > 0 and level < len(levels):
            self.create_meteors(level)
            
            while self.life_count > 0 and len(self.meteors) > 0:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()
                   
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        return False
                    if self.ship.ship_status == ShipStatus.explode:
                        return False

                self.background_change(self.current_time)

                self.all.update()

                for meteor in self.meteors:
                    if meteor.pass_meteor():
                        self.meteors.remove(meteor)
                        self.all.remove(meteor)
                        self.points += 1   
                        if len(self.meteors) == 0:
                            self.world.status_arrive = True

                if self.ship.ship_status == ShipStatus.travel:   
                    if pg.sprite.spritecollide(self.ship, self.meteors, True):
                        self.life_count -= 1
                        if self.life_count == 0:
                            self.ship.ship_status = ShipStatus.explode
                             
                self.screen.blit(self.background, (0,0))

                self.all.draw(self.screen)

                self.counters(level)

                pg.display.flip()

            #Bucle cuando llega al mundo
            while self.world.status_arrive == True:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        return False

                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.world.status_arrive = False

                self.all.update()

                if self.world.rect.centerx <= self.screen.get_width() + 450:
                    self.ship.ship_status = ShipStatus.arrive
                    if self.ship.rotation == 181:
                        self.ship.ship_status = ShipStatus.landing

                self.background_change(self.current_time)

                self.screen.blit(self.background, (0,0))

                self.all.draw(self.screen)

                self.counters(level)

                if self.ship.rect.right >= self.screen.get_width():
                    self.press_continue("Presione ESPACIO para continuar")

                pg.display.flip()

            level += 1
            self.ship.reset()
            self.world.reset()
            self.reset()
            
        self.write_records(self.points, self.life_count)
        return True

class Records(Scene):
    def __init__(self, screen, estado):
        super().__init__(screen)
        self.win_background = pg.image.load(os.path.join("./resources/images/Worlds/Arrive_World.png")).convert_alpha()
        self.lose_background = pg.image.load(os.path.join("./resources/images/Worlds/Earth_red.jpg")).convert_alpha()
        self.time = 0
        self.delay_pass = 1200
        self.estado = estado

    def bucle_ppal(self):
        self.time = 0
        while True:

            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return True
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return pg.quit()

            self.time += 1

            if self.time >= self.delay_pass:
                return True

            if self.estado == 1:
                self.screen.blit(self.win_background, (0, 0))
            elif self.estado == 0:
                self.screen.blit(self.lose_background, (0, 0))

            self.press_continue("Presione ESPACIO para volver al inicio")

            pg.display.flip()

    
