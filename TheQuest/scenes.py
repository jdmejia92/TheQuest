import pygame as pg
from TheQuest import FPS, levels, BigAsteroids
from TheQuest.entities import Explosion, Meteor, Ship, World, ShipStatus, ProcessData
import os
import sys
from enum import Enum
import random as rd

white = (255, 255, 255)
black = (0, 0, 0)

class Alternative_Ending(Enum):
    win_NewRecord = 1
    win_NoRecord = 2
    lose_NewRecord = 3
    lose_NoRecord = 4

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.font_press = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 20)
        self.data = ProcessData()
        self.clock = pg.time.Clock()
        self.delay = 1750
        self.current_time = pg.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.show = True
        self.delay_show = 110
        self.show_count = 0

    #Hacer que el texto parpadee
    def press_continue(self, texto):
        if self.current_time >= self.change_time:
            self.change_time = self.current_time + self.delay
            self.show = not self.show

        if self.show:
            press_continue = self.font_press.render(texto, True, white)
            rectexto_press = press_continue.get_rect()
            centerx = (self.screen.get_width() - rectexto_press.width)//2
            centery = (self.screen.get_height() - rectexto_press.h) - 30
            rect = pg.Surface((rectexto_press.w + 10, rectexto_press.h + 10))
            rect.set_alpha(128)
            rect.fill((black))
            self.screen.blit(rect, (centerx - 5, centery - 5))
            self.screen.blit(press_continue, (centerx, centery))

    def bucle_ppal(self) -> bool:
        return

class Intro(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.cover = pg.image.load("./resources/images/Worlds/Earth_red.jpg")
        self.font_title = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 60)      

    #Cargar los titulos una sola vez
    def title(self):
        title = self.font_title.render("THE QUEST", True, white)
        rectexto = title.get_rect()
        self.screen.blit(title, ((self.screen.get_width() - rectexto.width)//2, (self.screen.get_height() - rectexto.h)//2))

    #Letrero de pasar a la siguiente escena
    def press_nextscene(self):
        if self.show_count >= 80:
            self.press_continue("Presiona ESPACIO para iniciar")

    def bucle_ppal(self):
        while True:
            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            self.screen.blit(self.cover, (0, 0))

            self.title()

            self.show_count += 1
            
            self.press_nextscene()
            
            pg.display.flip()

class History(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.clock.tick(FPS)
        self.backgrounds = []
        self.active_background = 0
        self.how_many = 0
        self.animation_time = FPS//2
        self.move_background = True

        self.load_background()

        self.current_time = 0

    #Cargar el fondo
    def load_background(self):
        space = pg.image.load(os.path.join("./resources/images/Worlds/history.png")).convert_alpha()
        for fila in range(600):
            y = fila + 1

            image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
            image.blit(space, (0,0), (0, y, self.screen.get_width(), self.screen.get_height()))

            self.backgrounds.append(image)

        self.how_many = len(self.backgrounds)
        self.background = self.backgrounds[self.active_background]

    #Mover el fondo
    def background_change(self, dt):
        self.current_time += dt
        try:
            if self.move_background == True:
                if self.current_time > self.animation_time:
                    self.current_time = 0
                    self.active_background += 1
                    if self.active_background >= len(self.backgrounds):
                        self.move_background = False
                
                self.background = self.backgrounds[self.active_background]
        except IndexError:
            pass

    #Letrero de pasar a la siguiente escena
    def press_nextscene(self):
        if self.move_background == False:
            self.press_continue("Presione ESPACIO para continuar")

    def reset(self):
        self.current_time = 0
        self.active_background = 0
        self.move_background = True

    def bucle_ppal(self) -> bool:
        self.reset()
        while True:

            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return True
            
            self.current_time = pg.time.get_ticks()

            self.background_change(self.current_time)

            self.screen.blit(self.background, (0,0))

            self.press_nextscene()

            pg.display.flip()

class Play(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.font_counter = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 16)
        self.white_back = pg.image.load(os.path.join("./resources/images/input/Fondo_contadores.png")).convert_alpha()
        self.regular_background = pg.image.load(os.path.join("./resources/images/Background/New_Background.png")).convert_alpha()
        self.first_background_image = pg.image.load(os.path.join("./resources/images/Background/First_Background.png")).convert_alpha()
        self.ship = Ship(self.screen, 80, self.screen.get_height()//2)
        self.world = World(self.screen, self.screen.get_width() + 1000, self.screen.get_height()//2)
        #Lista de niveles
        self.meteors = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.all = pg.sprite.Group()
        self.points = 0
        self.count = 0
        self.clock.tick(FPS)

        #Listas de meteoros
        self.BigAsteroids = []
        self.levels = []

        #Lista con el fondo cargado
        self.first_backgrounds = []
        self.backgrounds = []
        self.first_level = True
        self.active_background = 0
        self.animation_time = FPS

        self.load_background(self.first_background_image, 1)
        self.load_background(self.regular_background, 0)

        self.current_time = 0

    #Carga del fondo
    def load_background(self, space, code):
        space_image = space
        if code == 0:
            for colum in range(1600):
                x = colum + 1

                image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
                image.blit(space_image, (0,0), (x, 0, self.screen.get_width(), self.screen.get_height()))

                self.backgrounds.append(image)

            self.background = self.backgrounds[self.active_background]

        elif code == 1:
            for colum in range(2000):
                x = colum + 1

                image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
                image.blit(space_image, (0,0), (x, 0, self.screen.get_width(), self.screen.get_height()))

                self.first_backgrounds.append(image)

            self.first_background = self.first_backgrounds[self.active_background]       

    #Moviemiento del fongo
    def background_move(self, dt):
        self.current_time += dt
        if self.ship.ship_status == ShipStatus.travel or self.ship.ship_status == ShipStatus.takeoff or self.ship.ship_status == ShipStatus.deploy or self.ship.ship_status == ShipStatus.lunch:
            if self.current_time > self.animation_time:
                self.current_time = 0
                self.active_background += 1
                if self.active_background >= len(self.backgrounds):
                    self.active_background = 0

                self.background = self.backgrounds[self.active_background]
    
    #Move first background
    def firstBackground_move(self, dt):
        self.current_time += dt
        if self.ship.ship_status == ShipStatus.travel or self.ship.ship_status == ShipStatus.takeoff or self.ship.ship_status == ShipStatus.deploy or self.ship.ship_status == ShipStatus.lunch:
            if self.current_time > self.animation_time:
                self.current_time = 0
                self.active_background += 1
                if self.active_background >= len(self.backgrounds):
                    self.first_level = False

                self.first_background = self.first_backgrounds[self.active_background]

    #Escoger entre el 1er background y el estandar
    def chose_background(self):
        if self.first_level == True:
            self.firstBackground_move(self.current_time)
            self.screen.blit(self.first_background, (0,0))
        elif self.first_level == False:
            self.background_move(self.current_time)
            self.screen.blit(self.background, (0,0))

    #Reinicio al pasar de nivel
    def reset(self):
        self.meteors.empty()
        self.asteroids.empty()
        self.obstacles.empty()
        self.all.empty()
        self.all.add(self.world, self.ship)
        self.ship.reset()
        self.world.reset()
        self.count = 0

    #Creacion de meteoros
    def create_meteors(self, level):
        for col, fil in self.levels[level]:
            m = Meteor(800 * col, 30 * fil, 1)
            self.meteors.add(m)
        self.obstacles.add(self.meteors)

    #Creacion de meteoros grandes
    def create_bigmeteors(self, asteroid):
        for col, fil in self.BigAsteroids[asteroid]:
            m = Meteor(800 * col, 30 * fil, 0)
            self.asteroids.add(m)
        self.obstacles.add(self.asteroids)
    
    #Eliminacion de meteoros
    def eliminate_meteors(self, group_rock):
        for rock in group_rock:
            if rock.pass_meteor():
                group_rock.remove(rock)
                self.obstacles.remove(rock)
                if group_rock == self.meteors:
                    self.points += 1
                elif group_rock == self.asteroids:
                    self.points += 2

            if self.ship.ship_status == ShipStatus.travel:
                hits = pg.sprite.spritecollide(self.ship, group_rock, True)
                for hit in hits:
                    if group_rock == self.meteors:
                        explosion = Explosion(hit.rect.center, 'Small')
                        self.all.add(explosion)
                        self.life_count -= 1
                    elif group_rock == self.asteroids:
                        explosion = Explosion(hit.rect.center, 'Big')
                        self.all.add(explosion)
                        self.life_count -= 2

            if self.life_count <= 0:
                if pg.sprite.collide_rect(self.ship, rock):
                    explosion = Explosion(self.ship.rect.center, 'Ship')
                    self.all.add(explosion)
                self.count += 1
                if self.count == 2000:
                    self.life_count -= 5
                print(self.count)

    #Contadores en pantalla
    def counters(self, level):
        self.screen.blit(self.white_back, (3, 5))
        life_text = self.font_counter.render('Contador de vidas: ' + str(self.life_count), True, white)
        level_text = self.font_counter.render('Level: ' + str(level + 1), True, white)
        points = self.font_counter.render('Puntos: ' + str(self.points), True, white)
        self.screen.blit(life_text, (10, 10))
        self.screen.blit(level_text, (10, 28))
        self.screen.blit(points, (10, 45))

    #Activar llegar al mundo al culminar los asteroides
    def next_level(self):
        if len(self.asteroids) == 0:
            self.world.status_arrive = True

    #Letrero de pasar a la siguiente escena
    def press_nextscene(self):
        if self.ship.rect.right >= self.screen.get_width():
            self.press_continue("Presione ESPACIO para continuar")

    #Crear lista de niveles
    def create_levels(self):
        for i in range(3):
            x_a = []
            for i in range(10):
                n = rd.uniform(1.5,15)
                x_a.append(n)
            y_a = []
            for i in range(10):
                m = rd.uniform(1,20)
                y_a.append(m)
            asteroid = list(zip(x_a, y_a))
            self.BigAsteroids.append(asteroid)

        for i in range(3):
            x = []
            for i in range(10):
                n = rd.uniform(1.5,15)
                x.append(n)
            y = []
            for i in range(10):
                m = rd.uniform(1,20)
                y.append(m)
            level = list(zip(x, y))
            self.levels.append(level)

    #Juego
    def bucle_ppal(self) -> bool:
        #Listas para niveles distintos en cada vuelta
        self.BigAsteroids = []
        self.levels = []
        #Constadores
        level = 0
        asteroid = 0
        self.life_count = 3
        self.points = 0
        #Resetear y creacion de niveles
        self.first_level = True
        self.active_background = 0
        self.create_levels()
        self.reset()

        while self.life_count > -2 and asteroid < len(self.BigAsteroids):
            self.create_meteors(level)
            self.create_bigmeteors(asteroid)
            
            while self.life_count > -2 and len(self.asteroids) > 0:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                self.chose_background()

                if self.ship.ship_status == ShipStatus.travel:
                    self.obstacles.update()

                if self.life_count <= 0:
                    self.ship.ship_status = ShipStatus.explode

                self.all.update()

                self.eliminate_meteors(self.meteors)
                self.eliminate_meteors(self.asteroids)

                self.next_level()

                self.all.draw(self.screen)
                self.obstacles.draw(self.screen)

                self.counters(level)

                pg.display.flip()

            #Bucle cuando llega al mundo
            while self.world.status_arrive == True:
                points_arrive = 0
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.world.status_arrive = False

                self.all.update()

                if self.world.rect.centerx == 1260:
                    points_arrive += 5
                
                self.points += points_arrive

                if self.world.rect.centerx <= self.screen.get_width() + 450:
                    self.ship.ship_status = ShipStatus.arrive
                    if self.ship.rotation == 181:
                        self.ship.ship_status = ShipStatus.landing

                self.background_move(self.current_time)

                self.screen.blit(self.background, (0,0))

                self.all.draw(self.screen)

                self.counters(level)

                self.press_nextscene()

                pg.display.flip()

            level += 1
            asteroid += 1
            self.reset()

        self.data.createdata()
        self.data.player_record(points = self.points, life = self.life_count)
        return True

class Records(Scene):
    def __init__(self, screen, estado):
        super().__init__(screen)
        self.win_background = pg.image.load(os.path.join("./resources/images/Worlds/Arrive_World.png")).convert_alpha()
        self.lose_background = pg.image.load(os.path.join("./resources/images/Worlds/Fail.png")).convert_alpha()
        self.font_initials = pg.font.Font("./resources/fonts/Techovier Bold.ttf", 29)
        self.font_points = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 60)
        self.input = pg.image.load(os.path.join("./resources/images/Input/Input.png")).convert_alpha()
        self.input_rect = self.input.get_rect(center=(self.screen.get_width()//2, 450))
        self.write_initials = pg.image.load(os.path.join("./resources/images/Worlds/Ingresa_iniciales.png")).convert_alpha()
        self.write_initials_rect = self.write_initials.get_rect()
        self.active = False
        self.estado = estado
        self.initials = ""    

    #Cargar fondos alternativos, segun acabe el juego
    def load_background(self):
        if self.estado == Alternative_Ending.win_NewRecord or self.estado == Alternative_Ending.win_NoRecord:
            self.screen.blit(self.win_background, (0, 0))
        elif self.estado == Alternative_Ending.lose_NewRecord or self.estado == Alternative_Ending.lose_NoRecord:
            self.screen.blit(self.lose_background, (0, 0))

    #Mostrar los puntos
    def show_points(self):
        points = self.data.show_points()
        text_points = self.font_points.render(str(points), True, white)
        self.screen.blit(text_points, (412.9, 284.9))
    
    #Solicitar ingresar los puntos en caso supere al 5to mas alto
    def input_initials(self):
        if self.estado == Alternative_Ending.lose_NewRecord or self.estado == Alternative_Ending.win_NewRecord:
            self.screen.blit(self.write_initials, (self.screen.get_width()//2 - self.write_initials_rect.centerx, self.screen.get_height()//2 + 55))
            self.screen.blit(self.input, (self.input_rect.x, self.input_rect.y))
            text_surface = self.font_initials.render(self.initials, True, white)
            self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 2))

    #Letrero para pasar a la siguiente escena
    def press_nextscene(self):
        if self.estado == Alternative_Ending.lose_NewRecord and len(self.initials) >= 3 or self.estado == Alternative_Ending.win_NewRecord and len(self.initials) >= 3:
            self.press_continue("Presione ENTER para continuar...")
        elif self.estado == Alternative_Ending.lose_NoRecord or self.estado == Alternative_Ending.win_NoRecord:
            self.press_continue("Presione ENTER para continuar...")

    def bucle_ppal(self):
        self.time = 0

        while True:

            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return True

                if self.estado == Alternative_Ending.win_NewRecord or self.estado == Alternative_Ending.lose_NewRecord:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.initials = self.initials[:-1]
                        else:
                            self.initials += event.unicode
                        if len(self.initials) > 3:
                            self.initials = self.initials[:3]

            self.load_background()

            self.show_points()
            self.input_initials()

            self.press_nextscene()

            pg.display.flip()

            self.initials = self.initials.upper()
            n = self.data.show_lastid()
            self.data.update(id = n, initials = self.initials)


class Ending(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.ending = pg.image.load("./resources/images/Worlds/Earth.png")
        self.rect = self.ending.get_rect()
        self.font_records = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 58)

    #Muestra los mejores 5 puntajes
    def show_records(self):
        self.positiony = 0
        records = self.data.show_records()
        for name, points in records:
            if name == "" or name == None:
                name = "###"                
            self.positiony += 75
            record_name = self.font_records.render(str(name), True, white)
            record_points = self.font_records.render(str(points), True, white)
            self.screen.blit(record_name, (270, 68 + self.positiony))
            self.screen.blit(record_points, (480, 68 + self.positiony))

    #Letrero para continuar a la siguiente escena
    def press_nextscene(self):
        if self.show_count >= 80:
            self.press_continue("Presiona ESPACIO para volver a iniciar")
        if self.show_count >= 2500:
            return True

    def deleteLowerPoint(self):
        point_play = self.data.show_points()
        fifth_point = self.data.lower_visible_point()
        if point_play <= fifth_point:
            id = self.data.show_lastid()
            self.data.deleteLowPoints(id)

    def bucle_ppal(self) -> bool:
        while True:
            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True
            
            self.screen.blit(self.ending, (0, 0))

            self.deleteLowerPoint()

            self.show_records()

            self.show_count += 1

            self.press_nextscene()

            pg.display.flip()