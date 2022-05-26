import pygame as pg
from TheQuest import FPS
from TheQuest.entities import Explosion, Meteor, Ship, World, ShipStatus, ProcessData
import os
import sys
from enum import Enum
import random as rd

white = (255, 255, 255)
black = (0, 0, 0)
music = True

class Alternative_Ending(Enum):
    win_NewRecord = 1
    win_NoRecord = 2
    lose_NewRecord = 3
    lose_NoRecord = 4

class Scene:
    def __init__(self, screen):
        self.screen = screen
        #Carga de fuentes para los textos regulares
        self.font_press = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 20)
        #Canciones
        self.sad_song = "./resources/music/Argonne - Zachariah Hickman.mp3"
        self.happy_song = "./resources/music/Panda Clan - DJ Williams.mp3"
        self.win_song = "./resources/music/Fond Memories - SYBS.mp3"
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

    #Parar la musica
    def stop_music(self):
        global music
        if music == True:
            pg.mixer.music.set_volume(0.5)
        elif music == False:
            pg.mixer.music.set_volume(0.0)  

    def bucle_ppal(self) -> bool:
        pass
            

class Intro(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        #Carga fondo y fuente para titulo principal
        self.cover = pg.image.load("./resources/images/Worlds/Earth_red.jpg")
        self.font_title = pg.font.Font("./resources/fonts/Dissimilar-Headlines.ttf", 60)
        self.controls = pg.image.load(os.path.join("./resources/images/Instructions/Controles.png")).convert_alpha()
        self.controls_rect = self.controls.get_rect()
        self.instruccions_image = pg.image.load(os.path.join("./resources/images/Instructions/Instructions.png")).convert_alpha()
        self.instruccions_image_rect = self.instruccions_image.get_rect(centerx = self.screen.get_width()//2, centery = self.screen.get_height()//2)
        self.show_instruccions = False

    #Cargar los textos una sola vez
    def texts(self):
        title = self.font_title.render("THE QUEST", True, white)
        rectexto = title.get_rect()
        self.screen.blit(title, ((self.screen.get_width() - rectexto.width)//2, (self.screen.get_height() - rectexto.h)//2))
        self.screen.blit(self.controls, ((10, 10)))

    #Letrero de pasar a la siguiente escena
    def press_nextscene(self):
        if self.show_count >= 80:
            self.press_continue("Presiona ESPACIO para iniciar")

    #Carga de musica
    def play_music(self):
        pg.mixer.music.load(self.sad_song, 'mp3')
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)

    #Mostrar las instrucciones
    def instruccions(self):
        if self.show_instruccions == True:
            self.screen.blit(self.instruccions_image, (self.instruccions_image_rect.x, self.instruccions_image_rect.y))

    def bucle_ppal(self):
        self.play_music()

        while True:
            self.stop_music()

            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    global music
                    if music == True:
                        music = False
                    elif music == False:
                        music = True
                if event.type == pg.KEYDOWN and event.key == pg.K_2:
                    if self.show_instruccions == False:
                        self.show_instruccions = True
                    elif self.show_instruccions == True:
                        self.show_instruccions = False

            self.screen.blit(self.cover, (0, 0))

            self.texts()

            self.instruccions()

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

    #Reinicio si se hace una segunda vuelta
    def reset(self):
        self.current_time = 0
        self.active_background = 0
        self.move_background = True

    def bucle_ppal(self) -> bool:
        self.reset()
        while True:
            self.stop_music()

            self.clock.tick(FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        return True

                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    global music
                    if music == True:
                        music = False
                    elif music == False:
                        music = True

            self.current_time = pg.time.get_ticks()

            self.background_change(self.current_time)

            self.screen.blit(self.background, (0,0))

            self.press_nextscene()

            pg.display.flip()

class Play(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.font_counter = pg.font.Font("./resources/fonts/FredokaOne-Regular.ttf", 16)
        self.regular_background = pg.image.load(os.path.join("./resources/images/Background/New_Background.png")).convert_alpha()
        self.first_background_image = pg.image.load(os.path.join("./resources/images/Background/First_Background.png")).convert_alpha()
        #Mostrar instrucciones y boton de controles
        self.instruccions_image = pg.image.load(os.path.join("./resources/images/Instructions/Instructions.png")).convert_alpha()
        self.instruccions_image_rect = self.instruccions_image.get_rect(centerx = self.screen.get_width()//2, centery = self.screen.get_height()//2)
        self.show_instruccions = False
        self.controls = pg.image.load(os.path.join("./resources/images/Instructions/Controles.png")).convert_alpha()
        self.controls_rect = self.controls.get_rect()
        #Carga jugador y mundos
        self.ship = Ship(self.screen, 80, self.screen.get_height()//2)
        self.world_start = World(self.screen, -400, self.screen.get_height()//2, "Start")
        self.midle_world = World(self.screen, self.screen.get_width() + 1000, self.screen.get_height()//2, "Midle")
        self.midle_world_lunch = World(self.screen, -400, self.screen.get_height()//2, "Midle_lunch")
        self.world = World(self.screen, self.screen.get_width() + 1000, self.screen.get_height()//2, "End")
        #Carga de sonidos de explosion
        self.explosion_big = pg.mixer.Sound("./resources/music/Explosion.wav")
        self.explosion_big.set_volume(0.2)
        self.explosion_small = pg.mixer.Sound("./resources/music/Explosion.wav")
        self.explosion_small.set_volume(0.1)
        self.explosion_ship = pg.mixer.Sound("./resources/music/Explosion.wav")
        self.explosion_ship.set_volume(0.5)
        #Lista de niveles
        self.worlds = pg.sprite.Group()
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
    def choose_background(self):
        if self.first_level == True:
            self.firstBackground_move(self.current_time)
            self.screen.blit(self.first_background, (0,0))
        elif self.first_level == False:
            self.background_move(self.current_time)
            self.screen.blit(self.background, (0,0))

    def choose_world(self, level):
        if self.life_count > 0:
            if level == 0:
                self.worlds.add(self.world_start, self.midle_world)
            elif level > 0 and level < len(self.BigAsteroids)-1:
                self.worlds.add(self.midle_world_lunch, self.midle_world)
            elif level == len(self.BigAsteroids)-1:
                self.midle_world.kill()
                self.worlds.add(self.midle_world_lunch, self.world)

    #Reinicio al pasar de nivel
    def reset(self):
        self.meteors.empty()
        self.asteroids.empty()
        self.obstacles.empty()
        self.worlds.empty()
        self.all.empty()
        self.choose_world(self.asteroid)
        self.all.add(self.worlds, self.ship)
        self.ship.reset()
        worlds = self.worlds
        for world in worlds:
            world.reset()
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
        global music
        for rock in group_rock:
            if rock.pass_meteor():
                group_rock.remove(rock)
                self.obstacles.remove(rock)
                if group_rock == self.meteors:
                    self.points += 1
                elif group_rock == self.asteroids:
                    self.points += 2

            if self.ship.ship_status == ShipStatus.travel:
                if pg.sprite.spritecollide(self.ship, group_rock, False):
                    hits = pg.sprite.spritecollide(self.ship, group_rock, True, pg.sprite.collide_mask)
                    for hit in hits:
                        if group_rock == self.meteors:
                            explosion = Explosion(hit.rect.center, 'Small')
                            self.all.add(explosion)
                            self.life_count -= 1
                            if music == True:
                                self.explosion_small.play()
                        elif group_rock == self.asteroids:
                            explosion = Explosion(hit.rect.center, 'Big')
                            self.all.add(explosion)
                            self.life_count -= 2
                            if music == True:
                                self.explosion_big.play()

            if self.life_count <= 0:
                if pg.sprite.collide_rect(self.ship, rock):
                    explosion = Explosion(self.ship.rect.center, 'Ship')
                    self.all.add(explosion)
                    if music == True:
                        self.explosion_ship.play()
                self.count += 1
                if self.count >= 6000:
                    self.ship.ship_status = ShipStatus.destroy

    #Contadores en pantalla
    def texts(self, level):
        life_text = self.font_counter.render('Contador de vidas: ' + str(self.life_count), True, white)
        rect_life_text = life_text.get_rect()
        back = pg.Surface((rect_life_text.w + 15, 65))
        back.set_alpha(85)
        back.fill((white))
        level_text = self.font_counter.render('Level: ' + str(level + 1), True, white)
        points = self.font_counter.render('Puntos: ' + str(self.points), True, white)
        self.screen.blit(back, (3, 5))
        self.screen.blit(life_text, (10, 10))
        self.screen.blit(level_text, (10, 28))
        self.screen.blit(points, (10, 45))
        self.screen.blit(self.controls, ((3, 75)))

    #Muestra las instrucciones
    def instructions(self):
        if self.show_instruccions == True:
            self.screen.blit(self.instruccions_image, (self.instruccions_image_rect.x, self.instruccions_image_rect.y))

    #Activar llegar al mundo al culminar los asteroides
    def world_arrive(self):
        if len(self.asteroids) <= 0 and self.asteroid < len(self.BigAsteroids) - 1 and self.life_count > 0:
            self.midle_world.status_arrive = True
        elif len(self.asteroids) <= 0 and self.asteroid == len(self.BigAsteroids) - 1 and self.life_count > 0:
            self.world.status_arrive = True

    #Acciones a la llegada a un nuevo mundo
    def worlds_accions(self):
        if self.midle_world.rect.centerx == 1272 or self.world.rect.centerx == 1272:
            self.points += 5
        #Que llegue el mundo medio
        if len(self.asteroids) <= 0 and self.asteroid < len(self.BigAsteroids) - 1:
            if self.midle_world.rect.centerx <= self.screen.get_width() + 500:
                self.ship.ship_status = ShipStatus.arrive
                if self.ship.rotation == 181:
                    self.ship.ship_status = ShipStatus.landing
        #Que llegue el mundo final
        elif len(self.asteroids) <= 0 and self.asteroid == len(self.BigAsteroids) - 1:
            if self.world.rect.centerx <= self.screen.get_width() + 450:
                self.ship.ship_status = ShipStatus.arrive
                if self.ship.rotation == 181:
                    self.ship.ship_status = ShipStatus.landing

    #Letrero de pasar a la siguiente escena
    def press_nextscene(self):
        if self.ship.rect.right >= self.screen.get_width():
            self.press_continue("Presione ESPACIO para continuar")

    #Crear lista de niveles
    def create_levels(self):
        for i in range(3):
            x_a = []
            for i in range(20):
                n = rd.uniform(1.1,10)
                x_a.append(n)
            y_a = []
            for i in range(20):
                m = rd.uniform(1,20)
                y_a.append(m)
            asteroid = list(zip(x_a, y_a))
            self.BigAsteroids.append(asteroid)

        for i in range(3):
            x = []
            for i in range(20):
                n = rd.uniform(1.1,10)
                x.append(n)
            y = []
            for i in range(20):
                m = rd.uniform(1,20)
                y.append(m)
            level = list(zip(x, y))
            self.levels.append(level)

    #Poner muscia dependiendo del nivel
    def play_music(self):
        if self.asteroid == 0:
            pg.mixer.music.load(self.sad_song, 'mp3')
            pg.mixer.music.set_volume(0.1)
            pg.mixer.music.play(fade_ms=5000, loops=-1)
        if self.asteroid >= 1:
            pg.mixer.music.load(self.happy_song, 'mp3')
            pg.mixer.music.set_volume(0.1)
            pg.mixer.music.play(fade_ms=5000, loops=-1)

    #Juego
    def bucle_ppal(self) -> bool:
        #Listas para niveles distintos en cada vuelta
        self.BigAsteroids = []
        self.levels = []
        #Constadores
        level = 0
        self.asteroid = 0
        self.life_count = 3
        self.points = 0
        #Resetear y creacion de niveles
        self.first_level = True
        self.active_background = 0
        self.create_levels()
        self.reset()

        while self.ship.ship_status != ShipStatus.destroy and self.asteroid < len(self.BigAsteroids):
            self.play_music()
            self.create_meteors(level)
            self.create_bigmeteors(self.asteroid)
            
            while self.ship.ship_status != ShipStatus.destroy and len(self.asteroids) > 0:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()
                self.stop_music()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN and event.key == pg.K_1:
                        global music
                        if music == True:
                            music = False
                        elif music == False:
                            music = True

                    if event.type == pg.KEYDOWN and event.key == pg.K_2:
                        if self.show_instruccions == False:
                            self.show_instruccions = True
                        elif self.show_instruccions == True:
                            self.show_instruccions = False

                if self.ship.ship_status == ShipStatus.travel:
                    self.obstacles.update()

                if self.life_count <= 0:
                    self.ship.ship_status = ShipStatus.explode

                self.eliminate_meteors(self.meteors)
                self.eliminate_meteors(self.asteroids)

                self.world_arrive()

                self.instructions()

                if self.show_instruccions == False:
                    self.choose_background()
                    self.all.update()
                    self.all.draw(self.screen)
                    self.obstacles.draw(self.screen)
                    self.texts(level)

                pg.display.flip()

            #Bucle cuando llega al mundo
            while self.midle_world.status_arrive == True or self.world.status_arrive == True:
                self.clock.tick(FPS)
                self.current_time = pg.time.get_ticks()

                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        self.world.status_arrive = False
                        self.midle_world.status_arrive = False

                    if event.type == pg.KEYDOWN and event.key == pg.K_2:
                        if self.show_instruccions == False:
                            self.show_instruccions = True
                        elif self.show_instruccions == True:
                            self.show_instruccions = False

                self.instructions()

                if self.show_instruccions == False:
                    self.all.update()
                    self.worlds_accions()
                    self.choose_background()
                    self.all.draw(self.screen)
                    self.texts(level)
                    self.press_nextscene()

                pg.display.flip()

            if self.life_count > 0:
                level += 1
                self.asteroid += 1
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
        self.input = pg.Rect(350, 427.5, 100, 45)
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
            text_surface = self.font_initials.render(self.initials, True, white)
            self.input.w = max(100, text_surface.get_width()+10)
            input = pg.Surface((self.input.w, self.input.h), pg.SRCALPHA)
            input.set_alpha(90)
            input.fill(white)
            self.screen.blit(input, (self.input.x, self.input.y))
            self.screen.blit(text_surface, (self.input.x + 5, self.input.y + 2))

    #Letrero para pasar a la siguiente escena
    def press_nextscene(self):
        if self.estado == Alternative_Ending.lose_NewRecord and len(self.initials) >= 3 or self.estado == Alternative_Ending.win_NewRecord and len(self.initials) >= 3:
            self.press_continue("Presione ENTER para continuar...")
        elif self.estado == Alternative_Ending.lose_NoRecord or self.estado == Alternative_Ending.win_NoRecord:
            self.press_continue("Presione ENTER para continuar...")

    def play_music(self):
        global music
        if music == True:
            if self.estado == Alternative_Ending.win_NewRecord or self.estado == Alternative_Ending.win_NoRecord:
                pg.mixer.music.load(self.win_song, 'mp3')
                pg.mixer.music.set_volume(0.1)
                pg.mixer.music.play(-1)
            elif self.estado == Alternative_Ending.lose_NewRecord or Alternative_Ending.lose_NoRecord:
                pg.mixer.music.load(self.sad_song, 'mp3')
                pg.mixer.music.set_volume(0.1)
                pg.mixer.music.play(-1)

    def bucle_ppal(self):
        self.play_music()
        self.time = 0

        while True:
            self.stop_music()

            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return True

                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    global music
                    if music == True:
                        music = False
                    elif music == False:
                        music = True

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
        self.show_count += 1
        if self.show_count >= 80:
            self.press_continue("Presiona ESPACIO para volver a iniciar")

    #Borrar el puntaje del jugador si es menor al 5to mas bajo
    def deleteLowerPoint(self):
        point_play = self.data.show_points()
        fifth_point = self.data.lower_visible_point()
        checkID = self.data.checkID
        if point_play <= fifth_point and checkID == False:
            id = self.data.show_lastid()
            self.data.deleteLowPoints(id)

    def bucle_ppal(self) -> bool:
        while True:
            self.stop_music()

            self.clock.tick(FPS)

            self.current_time = pg.time.get_ticks()

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return True
                
                if event.type == pg.KEYDOWN and event.key == pg.K_1:
                    global music
                    if music == True:
                        music = False
                    elif music == False:
                        music = True
            
            self.screen.blit(self.ending, (0, 0))

            self.deleteLowerPoint()

            self.show_records()

            self.press_nextscene()

            if self.show_count >= 1500:
                return True

            pg.display.flip()