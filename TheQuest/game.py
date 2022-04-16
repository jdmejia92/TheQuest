import pygame as pg
from TheQuest.scenes import Play, Intro, History, Records

pg.init()

class Game:
    def __init__(self, ancho=800, alto=600):
        screen = pg.display.set_mode((ancho, alto))
        pg.display.set_caption("The Quest")
        play = Play(screen)
        intro = Intro(screen)
        history = History(screen)
        records = Records(screen)
        self.scenes = [play]


    def deploy(self):
        active_escene = 0
        game_active = True
        while game_active:
            game_active = self.scenes[active_escene].bucle_ppal()
            active_escene += 1
            if active_escene == len(self.scenes):
                active_escene = 0
            
        