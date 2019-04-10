from Kabuki import Kabuki
import pygame
import sys
import numpy as np


toto = Kabuki(0, 0)
titi = Kabuki(5*toto.ecart, -5*toto.ecart, 0, (0, 255, 0))
tata = Kabuki(-5*toto.ecart, -5*toto.ecart, 0, (0, 0, 255))
tort = [toto, titi, tata]


def realtime(tortue=[Kabuki()], pas=0.1, eps=1., prop=1., inte=1.):
    pygame.init()
    clock = pygame.time.Clock()
    fenetre = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

    fond = pygame.Surface(fenetre.get_size())
    fond.fill((255, 255, 255))

    cible = pygame.Surface(fenetre.get_size())
    cible.fill((255, 255, 255))

    traine = pygame.Surface(fenetre.get_size())
    traine.set_colorkey((0, 0, 0))

    xcible = 0
    ycible = 0
    alpha = (np.pi/2)

    while 1:

        fenetre.blit(fond, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                xcible = (event.pos[0]-960)/20
                ycible = (-event.pos[1]+540)/20

                alpha = np.arctan2(ycible - tortue[0].y, xcible - tortue[0].x)

        pygame.draw.circle(cible, (0, 0, 255), (int(xcible*20)+960, int(-ycible*20)+540), 5)

        fenetre.blit(cible, (0, 0))

        tortue[0].rejoidre2(xcible, ycible, tortue[0].theta, eps, prop, inte, pas)

        tortue[1].rejoidre2(tortue[0].x+(5*tortue[0].ecart)*(-np.cos(alpha)+np.sin(alpha)), tortue[0].y+(5*tortue[0].ecart)*(-np.cos(alpha)-np.sin(alpha)), alpha, eps, prop, inte, pas)

        tortue[2].rejoidre2(tortue[0].x+(5*tortue[0].ecart)*(-np.cos(alpha)-np.sin(alpha)), tortue[0].y+(5*tortue[0].ecart)*(np.cos(alpha)-np.sin(alpha)), alpha, eps, prop, inte, pas)

        for k in range(len(tortue)):
            tortue[k].new_pos(pas)

            # for j in range(len(tortue[k].histx)):
            #
            #     x = int(tortue[k].histx[j])
            #     y = int(tortue[k].histy[j])
            #     traine.set_at((int(x*20)+960, -int(y*20)+540), tortue[k].color)
            #     fenetre.blit(traine, (0, 0))

            pygame.draw.circle(fenetre, tortue[k].color, (int(tortue[k].x*20)+960, int(-tortue[k].y*20)+540), int(tortue[k].ecart*40))

        pygame.display.flip()
        clock.tick(30)


        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


realtime(tort, 0.1, 1, 350, 10**(3))