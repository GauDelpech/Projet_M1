from Kabuki import Kabuki
import matplotlib.pyplot as plt
import pygame
import sys


toto = Kabuki(0, 0)
x = 10
y = 3

def realtime(tortue=Kabuki(), pas= 0.1, xcible=1, ycible=1, thetacible=0, eps=1):
    pygame.init()
    clock = pygame.time.Clock()
    fenetre = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

    fond = pygame.Surface(fenetre.get_size())
    fond.fill((255, 255, 255))

    traine = pygame.Surface(fenetre.get_size())
    traine.set_colorkey((0, 0, 0))

    while 1:

        tortue.rejoidre(xcible, ycible, thetacible, eps)

        tortue.new_pos(pas)

        fenetre.blit(fond, (0, 0))

        # for j in range(len(tortue.histx)):
        #     x = int(tortue.histx[j])
        #     y = int(tortue.histy[j])
        #     traine.set_at((int(x/5)+960, int(-y/5)+540), tortue.color)
        #     fenetre.blit(traine, (0, 0))

        pygame.draw.circle(fenetre, tortue.color, (int(tortue.x*20+960), int(-tortue.y*20+540)), int(tortue.ecart*40))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

def differe(tortue=Kabuki(), pas=0.1, nb_pas=1000, xcible=1, ycible=1, thetacible=0, eps=1):
    i=0

    while i <= nb_pas:

        toto.rejoidre(xcible, ycible, thetacible, eps)
        tortue.new_pos(pas)

        i += pas

    plt.plot(tortue.histx, tortue.histy)
    plt.title('Trajectoire du robot pour rejoindre la position (' + str(xcible) + ', ' + str(ycible) + ')')
    plt.show()


#differe(toto, 0.1, 1000, x, y)
realtime(toto, 0.1, x, y)
