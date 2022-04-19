from importlib import resources
from pickle import FALSE
from re import X
import pygame as pg
from TheQuest import FPS, levels
from TheQuest.entities import Meteor, Ship, World, ShipStatus
import os

white = (255, 255, 255)

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pg.time.Clock()

    def bucle_ppal(self) -> bool:
        return

class Intro(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.cover = pg.image.load("./resources/images/Intro/Earth_red.jpg")
        self.font_title = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 60)
        self.font_press = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 20)
        self.delay = 1200
        self.current_time = pg.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.show = True

       
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

            if self.current_time >= self.change_time:
                self.change_time = self.current_time + self.delay
                self.show = not self.show

            if self.show:
                press_continue = self.font_press.render("Presiona ESPACIO para iniciar", True, white)
                rectexto_press = press_continue.get_rect()
                self.screen.blit(press_continue, ((self.screen.get_width() - rectexto_press.width)//2,
                                             (self.screen.get_height() - rectexto_press.h) - 30))
            
            
            pg.display.flip()



class History(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.historia = pg.image.load("./resources/images/Intro/Earth_red.jpg")
        self.font_press = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 20)
        self.delay = 1200
        self.current_time = pg.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.show = True

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

            if self.current_time >= self.change_time:
                self.change_time = self.current_time + self.delay
                self.show = not self.show

            if self.show:
                press_continue = self.font_press.render("Presiona ESPACIO para iniciar", True, white)
                rectexto_press = press_continue.get_rect()
                self.screen.blit(press_continue, ((self.screen.get_width() - rectexto_press.width)//2,
                                             (self.screen.get_height() - rectexto_press.h) - 30))

            pg.display.flip()


class Play(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.font_counter = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 13)
        self.ship = Ship(self.screen, 80, self.screen.get_height()//2)
        self.world = World(self.screen, self.screen.get_width() + 1000, self.screen.get_height()//2)
        self.meteors = pg.sprite.Group()
        self.all = pg.sprite.Group()
        self.clock.tick(FPS)
        self.points = 0    

        #Carga del fondo movible
        self.backgrounds = []
        self.active_background = 0
        self.how_many = 0
        self.animation_time = FPS

        self.load_background()

        self.current_time = 0

    def load_background(self):
        space = pg.image.load(os.path.join("./resources/images/Background/New_Background.png")).convert_alpha()
        for colum in range(1600):
            x = colum + 1

            image = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA).convert_alpha()
            image.blit(space, (0,0), (x, 0, self.screen.get_width(), self.screen.get_height()))

            self.backgrounds.append(image)

        self.how_many = len(self.backgrounds)
        self.background = self.backgrounds[self.active_background]

    def background_change(self, dt):
        self.current_time += dt
        if self.ship.ship_status == ShipStatus.travel:
            if self.current_time > self.animation_time:
                self.current_time = 0
                self.active_background += 1
                if self.active_background >= len(self.backgrounds):
                    self.active_background = 0
                
                self.background = self.backgrounds[self.active_background]

        elif self.ship.ship_status == ShipStatus.arrive:
            self.background = self.backgrounds[self.active_background]

    def reset(self):
        self.meteors.empty()
        self.all.empty()
        self.all.add(self.world, self.ship)
        self.life_count = 3
        self.points = 0

    def create_meteors(self, level):
        for col, fil in levels[level]:
            m = Meteor(800 * col, 30 * fil)
            self.meteors.add(m)
        self.all.add(self.meteors)  

    def counters(self, level):
        life_text = self.font_counter.render('Contador de vidas: ' + str(self.life_count), True, (255, 255, 255))
        level_text = self.font_counter.render('Level: ' + str(level + 1), True, (255, 255, 255))
        points = self.font_counter.render('Puntos: ' + str(self.points), True, (255, 255, 255))
        self.screen.blit(life_text, (10, 10))
        self.screen.blit(level_text, (10, 30))
        self.screen.blit(points, (10, 50))
    
    def bucle_ppal(self) -> bool:
        level = 0
        self.reset()
                
        while self.life_count > 0 and level < len(levels):
            self.create_meteors(level)

            while self.life_count > 0 and len(self.meteors) > 0:    

                self.clock.tick(FPS)
                dt = pg.time.get_ticks()
                   
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        return False

                self.background_change(dt)

                self.all.update()

                for meteor in self.meteors:
                    if meteor.pass_meteor():
                        self.meteors.remove(meteor)
                        self.all.remove(meteor)
                        self.points += 1   

                if self.ship.ship_status == ShipStatus.travel:   
                    if pg.sprite.spritecollide(self.ship, self.meteors, True):
                        self.life_count -= 1

                if len(self.meteors) == 0:
                    self.world.status_arrive = True

                self.screen.blit(self.background, (0,0))

                self.all.draw(self.screen)

                self.counters(level)

                pg.display.flip()

            while self.world.status_arrive == True:
                self.clock.tick(FPS)
                dt = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        return False

                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.world.status_arrive = False

                self.all.update()

                if self.world.vx == 0:
                    self.ship.ship_status = ShipStatus.arrive
                    if self.ship.rotation == 181:
                        self.ship.ship_status = ShipStatus.landing

                self.background_change(dt)

                self.screen.blit(self.background, (0,0))

                self.all.draw(self.screen)

                self.counters(level)

                pg.display.flip()

            level += 1
            self.world.reset()
            self.ship.reset()
            self.reset()

        return True

class Records(Scene):
    def __init__(slef, screen):
        super().__init__(screen)
        pass
