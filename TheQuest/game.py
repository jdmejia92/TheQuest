import pygame as pg
from TheQuest.scenes import Play, Intro, History, Records, Ending, Alternative_Ending
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
        self.active_escene = 0

    def final_scenes(self):
        if self.active_escene == 3:
            n = ProcessData().show_life()
            p = ProcessData().show_points()
            m = ProcessData().lower_visible_point()
            print(m)
            print(p)
            if n <= 0 and p <= m:
                self.scenes.append(Records(self.screen, estado = Alternative_Ending.lose_NoRecord))
                self.scenes.append(self.ending)
            elif n > 0 and p <= m:
                self.scenes.append(Records(self.screen, estado = Alternative_Ending.win_NoRecord))
                self.scenes.append(self.ending)
            elif n <= 0 and p > m or n <= 0 and m == 0:
                self.scenes.append(Records(self.screen, estado = Alternative_Ending.lose_NewRecord))
                self.scenes.append(self.ending)
            elif n > 0 and p > m or n > 0 and m == 0:
                self.scenes.append(Records(self.screen, estado = Alternative_Ending.win_NewRecord))
                self.scenes.append(self.ending)
        
    def deploy(self):
        self.reset()
        game_active = True
        while game_active:
            try:
                game_active = self.scenes[self.active_escene].bucle_ppal()
            except IndexError:
                pass
            self.active_escene += 1
            self.final_scenes()      
            if self.active_escene > len(self.scenes):
                self.active_escene = 0
                self.data.con.close()
                self.reset()