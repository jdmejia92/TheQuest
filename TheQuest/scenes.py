import pygame as pg
from TheQuest import FPS, levels, BigAsteroids
from TheQuest.entities import Meteor, Ship, World, ShipStatus, ProcessData
import os
import sys

white = (255, 255, 255)
lightBlue = (68, 85, 90)


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

    #Texto que parpadee
    def press_continue(self, texto):
        if self.current_time >= self.change_time:
            self.change_time = self.current_time + self.delay
            self.show = not self.show

        if self.show:
            press_continue = self.font_press.render(texto, True, white)
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
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True
            
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

            self.screen.blit(self.cover, (0, 0))
            title = self.font_title.render("THE QUEST", True, white)
            rectexto = title.get_rect()

            self.screen.blit(title, ((self.screen.get_width() - rectexto.width)//2,
                                             (self.screen.get_height() - rectexto.h)//2))

            self.show_count += 1
            if self.show_count >= 80:
                self.press_continue("Presiona ESPACIO para iniciar")
            
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


    def load_background(self):
        space = pg.image.load(os.path.join("./resources/images/Worlds/history.png")).convert_alpha()
        for fila in range(600):
            y = fila + 1

            image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
            image.blit(space, (0,0), (0, y, self.screen.get_width(), self.screen.get_height()))

            self.backgrounds.append(image)

        self.how_many = len(self.backgrounds)
        self.background = self.backgrounds[self.active_background]

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


    def bucle_ppal(self) -> bool:
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

            if self.move_background == False:
                self.press_continue("Presione ESPACIO para continuar")

            pg.display.flip()

class Play(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.font_counter = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 16)
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
        self.ship.reset()
        self.world.reset()        

    #Creacion de meteoros
    def create_meteors(self, level):
        for col, fil in levels[level]:
            m = Meteor(800 * col, 30 * fil, 1)
            self.meteors.add(m)
        self.all.add(self.meteors)

    #Creacion de meteoros grandes
    def create_bigmeteors(self, asteroid):
        for col, fil in BigAsteroids[asteroid]:
            m = Meteor(800 * col, 30 * fil, 0)
            self.meteors.add(m)
        self.all.add(self.meteors)

    #Contadores en pantalla
    def counters(self, level):
        life_text = self.font_counter.render('Contador de vidas: ' + str(self.life_count), True, white)
        level_text = self.font_counter.render('Level: ' + str(level + 1), True, white)
        points = self.font_counter.render('Puntos: ' + str(self.points), True, white)
        self.screen.blit(life_text, (10, 10))
        self.screen.blit(level_text, (10, 28))
        self.screen.blit(points, (10, 45))

    #Juego
    def bucle_ppal(self) -> bool:
        level = 0
        asteroid = 0
        points = 0
        life_count = 3
        self.life_count = 3
        self.reset()

        while self.life_count > 0 and level < len(levels):
            self.create_meteors(level)
            self.create_bigmeteors(asteroid)
            
            while self.life_count > 0 and len(self.meteors) > 0:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if self.ship.ship_status == ShipStatus.explode:
                        return False

                self.background_change(self.current_time)

                self.all.update()
                
                #Eliminar meteoros
                for meteor in self.meteors:
                    if meteor.pass_meteor():
                        self.meteors.remove(meteor)
                        self.all.remove(meteor)
                        points += 1
                    elif pg.sprite.spritecollide(self.ship, self.meteors, True) and self.ship.ship_status == ShipStatus.travel:
                        life_count -= 1

                self.points = points
                self.life_count = life_count

                if self.life_count == 0:
                   self.ship.ship_status = ShipStatus.explode                 
                elif len(self.meteors) == 0:
                    self.world.status_arrive = True 

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
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.world.status_arrive = False

                self.all.update()

                if self.world.rect.centerx == 1255:
                    self.points += 5

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
            asteroid += 1
            self.reset()

        self.data.Createdata()
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
        self.active = False
        self.estado = estado
        self.initials = ""       
        

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

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.initials = self.initials[:-1]
                    else:
                        self.initials += event.unicode

                    if len(self.initials) > 3:
                        self.initials = self.initials[:3]

            if self.estado == True:
                self.screen.blit(self.win_background, (0, 0))
            elif self.estado == False:
                self.screen.blit(self.lose_background, (0, 0))

            self.screen.blit(self.input, (self.input_rect.x, self.input_rect.y))

            points = self.data.show_points()

            text_points = self.font_points.render(points, True, white)
            self.screen.blit(text_points, (412.9, 284.9))

            text_surface = self.font_initials.render(self.initials, True, white)
            self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 2))

            if len(self.initials) == 3:
                self.press_continue("Presione ENTER para continuar...")

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

            self.positiony = 0

            records = self.data.show_records()
            for name, points in records:
                self.positiony += 75
                record_name = self.font_records.render(str(name), True, white)
                record_points = self.font_records.render(str(points), True, white)
                self.screen.blit(record_name, (270, 68 + self.positiony))
                self.screen.blit(record_points, (480, 68 + self.positiony))

            self.show_count += 1
            if self.show_count >= 80:
                self.press_continue("Presiona ESPACIO para volver a iniciar")

            self.show_count += 1

            if self.show_count >= 2500:
                return True
            
            pg.display.flip()

    
