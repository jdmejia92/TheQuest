import random as rd

FPS = 60

BigAsteroids = []

#Lista valores de x de los asteroides grandes
for i in range(3):
    x_a = []
    for i in range(30):
        n = rd.uniform(1,14)
        x_a.append(n)

#Lista valores de y de los asteroides grandes
    y_a = []
    for i in range(30):
        m = rd.uniform(0,23)
        y_a.append(m)

#Crear la lista de tuplas para los grandes asteroides
    level = list(zip(x_a, y_a))
    BigAsteroids.append(level)

levels = []

#Lista valores de x de los meteoros pequeños
for i in range(3):
    x = []
    for i in range(30):
        n = rd.uniform(1,14)
        x.append(n)

#Lista valores de y de los meteoros pequeños
    y = []
    for i in range(30):
        m = rd.uniform(0,23)
        y.append(m)

#Crear la lista de tuplas para los meteoros pequeños
    level = list(zip(x, y))
    levels.append(level)