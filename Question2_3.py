from Kabuki import Kabuki
import matplotlib.pyplot as plt
import pygame
import sys




toto = Kabuki(0, 0)


def differe(tortue=Kabuki(), pas=0.1, nb_pas=1000):
    i=0
    j=0
    vt=0.1
    vr = -vt


    while i <= nb_pas:

        # if int(j) == 314:
        #     j=0
        #     vr = -vr

        toto.control(vt, vr)

        tortue.new_pos(pas)
        j += 1
        i += pas

    plt.plot(tortue.histx, tortue.histy)
    plt.title('Trajectoire du robot pour vtrans =' + str(vt) + ' et vrot = ' +  str(vr))
    plt.show()


def realtime(tortue=Kabuki(), pas=0.1):
    pygame.init()  # initialise pygame
    clock = pygame.time.Clock()  # initialise l'hotloge utilisé par pygame
    fenetre = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)  # initialise la fenêtre d'affichage

    fond = pygame.Surface(fenetre.get_size())  # surface fond blanc
    fond.fill((255, 255, 255))  # replie la surface de blanc

    traine = pygame.Surface(fenetre.get_size())  # surface permetant d'afficher la traîné
    traine.set_colorkey((0, 0, 0))  # Rend transparent les éléments noir de la surface

    while 1:  # boucle d'affichage

        tortue.new_pos(pas) # calcule un nouveau pas

        fenetre.blit(fond, (0, 0))  # applique le fond à la fenêtre

        for j in range(len(tortue.histx)):  # calcul de la traîné
            x = int(tortue.histx[j])
            y = int(tortue.histy[j])
            traine.set_at((int(x/5)+960, -int(y/5)+540), tortue.color)  # applique le nouveau point à la traîné
            fenetre.blit(traine, (0, 0))  # applique la traîné à la fenêtre

        pygame.draw.circle(fenetre, tortue.color, (int(tortue.x/5+960), int(-tortue.y/5+540)), int(tortue.ecart/10))
        # dessine le cercle repésentant le robot

        pygame.display.flip()  # affiche la fenêtre
        clock.tick(30)  # affiche à 30 fps

        for event in pygame.event.get():  # si on clique sur "quitter" le programme s'arrête
            if event.type == pygame.QUIT: sys.exit()


#realtime(toto)
differe(toto)