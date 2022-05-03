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
        
    def deploy(self):
        self.active_escene = 0
        game_active = True
        while game_active:
            game_active = self.scenes[self.active_escene].bucle_ppal()
            self.active_escene += 1
            if self.active_escene == 3:
                n = ProcessData().show_life()
                if n <= 0:
                    self.scenes.append(Records(self.screen, estado = False))
                    self.scenes.append(self.ending)
                elif n > 0:
                    self.scenes.append(Records(self.screen, estado = True))
                    self.scenes.append(self.ending)
            elif self.active_escene >= len(self.scenes):
                self.active_escene = 0
                self.data.con.close()
                self.reset()