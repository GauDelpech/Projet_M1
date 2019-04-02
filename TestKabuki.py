from Kabuki import Kabuki
import matplotlib.pyplot as plt
import pygame
import sys


toto = Kabuki(0, 0)
toto.set_speed(10, 5)

# for i in range(10000):
#     tortue.new_pos(0.1)
#
# plt.plot(tortue.histx, tortue.histy)
# plt.show()


def realtime(tortue=Kabuki(), pas=0.1, nb_pas=1000):
    pygame.init()
    clock = pygame.time.Clock()
    fenetre = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

    fond = pygame.Surface(fenetre.get_size())
    fond.fill((255,255,255))

    traine = pygame.Surface(fenetre.get_size())
    traine.set_colorkey((0,0,0))

    while 1:

        for i in range(nb_pas):
            tortue.new_pos(pas)

            fenetre.blit(fond, (0, 0))

            for j in range(len(tortue.histx)):
                x = int(tortue.histx[j])
                y = int(tortue.histy[j])
                traine.set_at((x+960, y+540), tortue.color)
                fenetre.blit(traine, (0, 0))

            pygame.draw.circle(fenetre, tortue.color, (int(tortue.x+960), int(tortue.y+540)), int(tortue.ecart))

            pygame.display.flip()
            clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()