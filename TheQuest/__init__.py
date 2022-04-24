import random as rd

FPS = 60

BigAsteroids = [
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(3,8),rd.uniform(1,5)), (rd.uniform(5,10),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,14),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(3,7)), (rd.uniform(5,10),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,14),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(7,10)), (rd.uniform(5,10),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,14),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25)), 
        (rd.uniform(1,5),rd.uniform(19,25)), (rd.uniform(3,8),rd.uniform(19,25)), (rd.uniform(5,10),rd.uniform(19,25)), (rd.uniform(10,11),rd.uniform(19,25)), (rd.uniform(12,14),rd.uniform(19,25)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25))], 
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(3,8),rd.uniform(1,5)), (rd.uniform(5,10),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,14),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(3,7)), (rd.uniform(5,10),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,14),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(7,10)), (rd.uniform(5,10),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,14),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25)), 
        (rd.uniform(1,5),rd.uniform(19,25)), (rd.uniform(3,8),rd.uniform(19,25)), (rd.uniform(5,10),rd.uniform(19,25)), (rd.uniform(10,11),rd.uniform(19,25)), (rd.uniform(12,14),rd.uniform(19,25)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25))],
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(3,8),rd.uniform(1,5)), (rd.uniform(5,10),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,14),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(3,7)), (rd.uniform(5,10),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,14),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(3,8),rd.uniform(7,10)), (rd.uniform(5,10),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,14),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25)), 
        (rd.uniform(1,5),rd.uniform(19,25)), (rd.uniform(3,8),rd.uniform(19,25)), (rd.uniform(5,10),rd.uniform(19,25)), (rd.uniform(10,11),rd.uniform(19,25)), (rd.uniform(12,14),rd.uniform(19,25)), 
        (rd.uniform(1,5),rd.uniform(20,25)), (rd.uniform(3,8),rd.uniform(20,25)), (rd.uniform(5,10),rd.uniform(20,25)), (rd.uniform(10,11),rd.uniform(20,25)), (rd.uniform(12,14),rd.uniform(20,25))]
        ]

levels = [
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(2,6),rd.uniform(1,5)), (rd.uniform(7,9),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,13),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(2,6),rd.uniform(3,7)), (rd.uniform(7,9),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,13),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(7,10)), (rd.uniform(2,6),rd.uniform(7,10)), (rd.uniform(7,9),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,13),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(10,15)), (rd.uniform(2,6),rd.uniform(10,15)), (rd.uniform(7,9),rd.uniform(10,15)), (rd.uniform(10,11),rd.uniform(10,15)), (rd.uniform(12,13),rd.uniform(10,15)), 
        (rd.uniform(1,5),rd.uniform(16,20)), (rd.uniform(2,6),rd.uniform(16,20)), (rd.uniform(7,9),rd.uniform(16,20)), (rd.uniform(10,11),rd.uniform(16,20)), (rd.uniform(12,13),rd.uniform(16,20)), 
        (rd.uniform(1,5),rd.uniform(25,40)), (rd.uniform(2,6),rd.uniform(25,40)), (rd.uniform(7,9),rd.uniform(25,40)), (rd.uniform(10,11),rd.uniform(25,40)), (rd.uniform(12,13),rd.uniform(25,40))],
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(2,6),rd.uniform(1,5)), (rd.uniform(7,9),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,13),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(2,6),rd.uniform(3,7)), (rd.uniform(7,9),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,13),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(7,10)), (rd.uniform(2,6),rd.uniform(7,10)), (rd.uniform(7,9),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,13),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(10,15)), (rd.uniform(2,6),rd.uniform(10,15)), (rd.uniform(7,9),rd.uniform(10,15)), (rd.uniform(10,11),rd.uniform(10,15)), (rd.uniform(12,13),rd.uniform(10,15)), 
        (rd.uniform(1,5),rd.uniform(16,20)), (rd.uniform(2,6),rd.uniform(16,20)), (rd.uniform(7,9),rd.uniform(16,20)), (rd.uniform(10,11),rd.uniform(16,20)), (rd.uniform(12,13),rd.uniform(16,20)), 
        (rd.uniform(1,5),rd.uniform(25,40)), (rd.uniform(2,6),rd.uniform(25,40)), (rd.uniform(7,9),rd.uniform(25,40)), (rd.uniform(10,11),rd.uniform(25,40)), (rd.uniform(12,13),rd.uniform(25,40))],
        [(rd.uniform(1,5),rd.uniform(1,5)), (rd.uniform(2,6),rd.uniform(1,5)), (rd.uniform(7,9),rd.uniform(1,5)), (rd.uniform(10,11),rd.uniform(1,5)), (rd.uniform(12,13),rd.uniform(1,5)), 
        (rd.uniform(1,5),rd.uniform(3,7)), (rd.uniform(2,6),rd.uniform(3,7)), (rd.uniform(7,9),rd.uniform(3,7)), (rd.uniform(10,11),rd.uniform(3,7)), (rd.uniform(12,13),rd.uniform(3,7)), 
        (rd.uniform(1,5),rd.uniform(7,10)), (rd.uniform(2,6),rd.uniform(7,10)), (rd.uniform(7,9),rd.uniform(7,10)), (rd.uniform(10,11),rd.uniform(7,10)), (rd.uniform(12,13),rd.uniform(7,10)), 
        (rd.uniform(1,5),rd.uniform(10,15)), (rd.uniform(2,6),rd.uniform(10,15)), (rd.uniform(7,9),rd.uniform(10,15)), (rd.uniform(10,11),rd.uniform(10,15)), (rd.uniform(12,13),rd.uniform(10,15)), 
        (rd.uniform(1,5),rd.uniform(16,20)), (rd.uniform(2,6),rd.uniform(16,20)), (rd.uniform(7,9),rd.uniform(16,20)), (rd.uniform(10,11),rd.uniform(16,20)), (rd.uniform(12,13),rd.uniform(16,20)), 
        (rd.uniform(1,5),rd.uniform(25,40)), (rd.uniform(2,6),rd.uniform(25,40)), (rd.uniform(7,9),rd.uniform(25,40)), (rd.uniform(10,11),rd.uniform(25,40)), (rd.uniform(12,13),rd.uniform(25,40))]
        ]