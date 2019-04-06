from Kabuki import Kabuki
import pygame
import sys


toto = Kabuki(0, 0)


def realtime(tortue=Kabuki(), pas=0.1, xcible=1, ycible=1, thetacible=0, eps=1., prop=1., inte=1.):
    pygame.init()
    clock = pygame.time.Clock()
    fenetre = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

    fond = pygame.Surface(fenetre.get_size())
    fond.fill((255, 255, 255))

    cible = pygame.Surface(fenetre.get_size())
    cible.fill((255, 255, 255))

    traine = pygame.Surface(fenetre.get_size())
    traine.set_colorkey((0, 0, 0))

    while 1:

        tortue.rejoidre2(xcible, ycible, thetacible, eps, prop, inte, pas)

        tortue.new_pos(pas)

        fenetre.blit(fond, (0, 0))

        # for j in range(len(tortue.histx)):
        #     x = int(tortue.histx[j])
        #     y = int(tortue.histy[j])
        #     traine.set_at((x+960, y+540), tortue.color)
        #     fenetre.blit(traine, (0, 0))

        pygame.draw.circle(cible, (0,0,255), (xcible+960, ycible+540), 5)
        fenetre.blit(cible, (0, 0))

        pygame.draw.circle(fenetre, tortue.color, (int(tortue.x+960), int(-tortue.y+540)), int(tortue.ecart))

        pygame.display.flip()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


realtime(toto, 0.1, 300, 0, 0, 1, 300, 100)