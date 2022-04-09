import pygame as pg
from TheQuest import FPS, levels
from TheQuest.entities import Meteor, Ship

white = (255, 255, 255)

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.reloj = pg.time.Clock()

    def bucle_ppal(self) -> bool:
        pass


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

            self.reloj.tick(FPS)

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

            self.reloj.tick(FPS)

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
        self.backgrounds = []
        for i in range(169):
            self.backgrounds.append(pg.image.load(f"./resources/images/Background/Espacio{i}.png"))
        self.delay = 1500
        self.active_background = 0
        self.change_frequency = 5
        self.frames_count = 0
        self.ship = Ship(self.screen, 80, self.screen.get_width()//2)
        self.meteors = pg.sprite.Group()
        self.all = pg.sprite.Group()

        self.background = self.backgrounds[self.active_background]
        self.current_time = pg.time.get_ticks()
        self.change_time = self.current_time + self.delay

    def background_change(self):
        self.frames_count += 1
        if self.frames_count == self.change_frequency:
            self.active_background += 1
            if self.active_background >= len(self.backgrounds):
                self.active_background = 0
            
            self.frames_count = 0

            self.background = self.backgrounds[self.active_background]

    def reset(self):
        self.meteors.empty()
        self.all.empty()
        self.all.add(self.ship)

    """def create_meteors(self, level):"""
        
        
    def bucle_ppal(self) -> bool:
        level = 0
        self.reset()

        while level < len(levels):
            self.current_time = pg.time.get_ticks()
            for col, fil, in levels[level]:
                if self.current_time >= self.change_time:
                    self.change_time = self.current_time + self.delay
                    m = Meteor(850 * col, 30 * fil)
                    self.meteors.add(m)
            self.all.add(self.meteors)

            while len(self.meteors) > 0:

                self.reloj.tick(FPS)

                events = pg.event.get()
                for event in events:
                    if event.type == pg.QUIT:
                        return False

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            return pg.quit()
                
                self.screen.blit(self.background, (0, 0))

                self.all.update()

                for meteor in self.meteors:
                    if meteor.pass_meteor():
                        self.meteors.remove(meteor)
                        self.all.remove(meteor)

                self.all.draw(self.screen)

                self.background_change()

                pg.display.flip()

            return True



class Records(Scene):
    def __init__(slef, screen):
        super().__init__(screen)
        pass
