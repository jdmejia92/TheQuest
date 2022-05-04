import pygame as pg
from TheQuest.scenes import Play, Intro, History, Records, Ending
from TheQuest.entities import ProcessData

pg.init()

class Game:
    def __init__(self, ancho=800, alto=600):
        self.screen = pg.display.set_mode((ancho, alto))
        pg.display.set_caption("The Quest")
        self.data = ProcessData()
        self.play = Play(self.screen)
        self.intro = Intro(self.screen)
        self.history = History(self.screen)
        self.ending = Ending(self.screen)
        self.scenes = [self.intro, self.history, self.play]
        self.active_scene = 0

    def reset(self):
        self.scenes.clear()
        scenes = [self.intro, self.history, self.play]
        self.scenes.extend(scenes)

    def process_data(self):
        try:
            m = ProcessData().lower_visible_point()
            return m
        except IndexError:
            return int(0)
        
    def deploy(self):
        self.active_escene = 0
        game_active = True
        while game_active:
            game_active = self.scenes[self.active_escene].bucle_ppal()
            self.active_escene += 1
            if self.active_escene == 3:
                n = ProcessData().show_life()
                p = ProcessData().show_points()
                m = self.process_data()
                if n <= 0 and p < m:
                    self.scenes.append(Records(self.screen, estado = 2))
                    self.scenes.append(self.ending)
                elif n > 0 and p < m:
                    self.scenes.append(Records(self.screen, estado = 1))
                    self.scenes.append(self.ending)
                elif n <= 0 and p > m or n <= 0 and m == 0:
                    self.scenes.append(Records(self.screen, estado = 4))
                    self.scenes.append(self.ending)
                elif n > 0 and p > m:
                    self.scenes.append(Records(self.screen, estado = 3))
                    self.scenes.append(self.ending)
            elif self.active_escene >= len(self.scenes):
                self.active_escene = 0
                self.data.con.close()
                self.reset()