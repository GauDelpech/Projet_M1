import numpy as np
from Moteur import MoteurCC
from Moteur import Controleur

class Kabuki(object):

    def __init__(self, x=0, y=0, theta=0, color=(250, 0, 0)):

        self.vg = 0
        self.vd = 0

        self.x = x
        self.y = y
        self.theta = theta

        self.v = 0
        self.vtheta = 0

        self.rayon = 37.5*0.001
        self.ecart = 351.5*0.001

        self.histx = [x]
        self.histy = [y]

        self.color = color

        self.moteurg = MoteurCC(1.5506, 0.00151, 0.010913, ((1/830)*(2*np.pi/60)), 0.006609, 0)
        self.moteurd = MoteurCC(1.5506, 0.00151, 0.010913, ((1 / 830) * (2 * np.pi / 60)), 0.006609, 0)
        self.controlg = Controleur(0,0)
        self.controld = Controleur(0,0)

        self.mvt = 0

    # def set_pos(self, x, y, theta):
    #     self.x = x
    #     self.y = y
    #     self.theta = theta
    #
    # def get_pos(self):
    #     return [self.x, self.y, self.theta]

    def set_speed(self, vg, vd):
        self.vg = vg
        self.vd = vd

        self.v = (self.rayon/2)*(self.vd + self.vg)
        self.vtheta = (self.rayon/self.ecart)*(self.vd-self.vg)

    def new_pos(self, dt):

        self.theta += self.vtheta*dt

        vx = self.v*(-np.sin(self.theta))  # nouvelle vitesse en x
        vy = self.v*np.cos(self.theta)  # nouvelle vitesse en y

        self.x += vx*dt
        self.y += vy*dt

        self.histx.append(self.x)  # enregistrement
        self.histy.append(self.y)

    def control(self, vtrans, vrot):

        self.vg = (vtrans - ((self.ecart*vrot)/2))/self.rayon
        self.vd = (vtrans + ((self.ecart*vrot)/2))/self.rayon

        self.set_speed(self.vg, self.vd)

    def clear(self):
        self.histx = []
        self.histy = []

    def control2(self, vtrans, vrot, p, i, dt):

        vg = (vtrans - ((self.ecart*vrot)/2))/self.rayon # MCI
        vd = (vtrans + ((self.ecart*vrot)/2))/self.rayon

        self.controlg.vd = vg  # On applique les valeurs aux controleurs
        self.controlg.va = self.vg

        self.controld.vd = vd  # On applique les valeurs aux controleurs
        self.controld.va = self.vd


        ug = self.controlg.pi(p, i, dt)  # PI donne la tension pour le moteur
        ud = self.controld.pi(p, i, dt)

        vg = self.moteurg.volt_to_speed2(ug, self.vg, dt)  # Calcul de la nouvelle vitesse
        vd = self.moteurd.volt_to_speed2(ud, self.vd, dt)

        self.set_speed(vg, vd) # Application de la vitesse

    def rejoidre(self, x_target, y_target, theta_target, eps):
        alpha = np.arctan2((y_target-self.y), (x_target-self.x))    # Calcul de l'angle entre l'horizontal et la cible

        if (x_target-eps < self.x < x_target + eps) and (y_target-eps < self.y < y_target + eps): # Si le robot est sur la cible
            if (theta_target-self.theta) > eps/10:  # Si le robot est mal orienté positivement par rapport à theta_target, il s'oriente
                self.control(0, theta_target-self.theta)

            elif (theta_target-self.theta) < -eps/10:  # Si le robot est mal orienté négativement par rapport à theta_target, il s'oriente
                self.control(0, theta_target-self.theta)

            else:   # Si le robot est bien orienté, il s'arrête
                self.control(0, 0)

        # Si le robot n'est pas encore sur la cible
        elif (alpha-self.theta) > (np.pi/2)+eps/10:  # Si le robot est mal orienté positivement par rapport à la cible, il s'oriente
            self.control(0, alpha-self.theta-(np.pi/2))

        elif (alpha-self.theta) < (np.pi/2)-eps/10:  # Si le robot est mal orienté négativement par rapport à la cible, il s'oriente
            self.control(0, alpha-self.theta-(np.pi/2))

        else:  # Si le robot est bien orienté par rapport à la cible, il avance tout droit
            self.control(np.sqrt((x_target-self.x)**2+(y_target - self.y)**2), 0)

    def rejoidre2(self, x_target, y_target, theta_target, eps, p, i, dt):
        alpha = np.arctan2((y_target-self.y), (x_target-self.x))

        if (x_target-eps < self.x < x_target + eps) and (y_target-eps < self.y < y_target + eps):

            if (theta_target-self.theta) > +eps/10:
                if self.mvt != +3:
                    self.controlg.clear()
                    self.controld.clear()
                self.mvt = +3

                self.control2(0, theta_target-self.theta, p, i, dt)

            elif (theta_target-self.theta) < -eps/10:
                if self.mvt != -3:
                    self.controlg.clear()
                    self.controld.clear()
                self.mvt = -3

                self.control2(0, theta_target-self.theta, p, i, dt)

            else:
                if self.mvt != 0:
                    self.controlg.clear()
                    self.controld.clear()
                self.mvt = 0
                self.control2(0, 0, p, i, dt)

        elif (alpha-self.theta) > (np.pi/2)+eps/10:
            if self.mvt != +1:
                self.controlg.clear()
                self.controld.clear()
            self.mvt=+1

            self.control2(0, alpha-self.theta-(np.pi/2), p, i, dt)

        elif (alpha-self.theta) < (np.pi/2)-eps/10:
            if self.mvt != -1:
                self.controlg.clear()
                self.controld.clear()
            self.mvt=-1

            self.control2(0, alpha-self.theta-(np.pi/2), p, i, dt)

        else:
            if self.mvt != 2:
                self.controlg.clear()
                self.controld.clear()
            self.mvt = 2

            self.control2(np.sqrt((x_target-self.x)**2+(y_target - self.y)**2), 0, p, i, dt)

    def UDPinstruction(self, ip, port):
        import socket

        UDP_IP_ADDRESS = ip
        UDP_PORT_NO = port

        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Création du socket

        UDPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
        # liaison du socket à l'ip et au port

        data = 'none'

        while data != 'exitUDP':  # si le message est 'exitUDP' on arrête l'écoute

            data, addr = UDPSock.recvfrom(1024)  #Ecoute

            # On s'attend à ce que data soit un string de la forme "cNb1Nb2" où
            # 1er lettre : "c" ou "v", c = instruction de coordonnées, v instruction de vitesse
            # lettres 2 à 4 est la coordonné en x ou la vitesse de translation
            # lettres 5 à 7 est la coordonné en y ou la vitesse de rotation

            if type(data) is str and len(data) == 7:  # vérification du format de l'information
                return data