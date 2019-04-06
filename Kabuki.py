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

        self.rayon = 1.9 #37.5 / 20
        self.ecart = 17.6 #351.5 / 20

        self.histx = [x]
        self.histy = [y]

        self.color = color

        self.moteurg = MoteurCC(1.5506, 0.00151, 0.010913, ((1/830)*(2*np.pi/60)), 0.006609, 0)
        self.moteurd = MoteurCC(1.5506, 0.00151, 0.010913, ((1 / 830) * (2 * np.pi / 60)), 0.006609, 0)
        self.controlg = Controleur(0,0)
        self.controld = Controleur(0,0)

        self.mvt = 0

    def set_pos(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def get_pos(self):
        return [self.x, self.y, self.theta]

    def set_speed(self, vg, vd):
        self.vg = vg
        self.vd = vd

        self.v = (self.rayon / 2)*(self.vd + self.vg)
        self.vtheta = (1/2)*(self.rayon/self.ecart)*(self.vd-self.vg)

    def new_pos(self, dt):

        self.theta += self.vtheta*dt

        vx = self.v*(-np.sin(self.theta))
        vy = self.v*np.cos(self.theta)

        self.x += vx*dt
        self.y += vy*dt

        self.histx.append(self.x)
        self.histy.append(self.y)

    def clear(self):
        self.histx = []
        self.histy = []

    def control(self, vtrans, vrot):
        eps_t = vtrans - self.v
        eps_r = vrot - self.vtheta

        self.vg += (2*eps_t - self.ecart*eps_r)/(2*self.rayon)
        self.vd += (2*eps_t + self.ecart*eps_r)/(2*self.rayon)

        self.set_speed(self.vg, self.vd)

    def control2(self, vtrans, vrot, p, i, dt):

        vg = 0
        vd = 0

        eps_t = vtrans - self.v
        eps_r = vrot - self.vtheta

        vg += (2 * eps_t - self.ecart * eps_r) / (2 * self.rayon)
        vd += (2 * eps_t + self.ecart * eps_r) / (2 * self.rayon)


        self.controlg.vd = vg
        self.controlg.va = self.vg

        self.controld.vd = vd
        self.controld.va = self.vd


        ug = self.controlg.pi(p, i, dt)
        ud = self.controld.pi(p, i, dt)

        vg = self.moteurg.volt_to_speed2(ug, self.vg, dt)
        vd = self.moteurd.volt_to_speed2(ud, self.vd, dt)

        self.set_speed(vg, vd)

    def rejoidre(self, x_target, y_target, theta_target, speed, eps):
        alpha = np.arctan2((y_target-self.y), (x_target-self.x))
        print('Alpha =  ' + str(alpha))

        if (x_target-eps < self.x < x_target + eps) and (y_target-eps < self.y < y_target + eps):
            if (theta_target-self.theta) > eps/5:
                self.control(0, speed)

            elif (theta_target-self.theta) < -eps/5:
                self.control(0, -speed)

            else:
                self.set_speed(0, 0)

        elif (alpha-self.theta) > (np.pi/2)+eps/5:
            self.control(0, speed)

            print('Theta =  ' + str(self.theta))
            print('orientation + :  delta = ' + str(alpha-self.theta))
            print('limite sup :  ' + str((np.pi/2)+eps/5))
            print('-------------')

        elif (alpha-self.theta) < (np.pi/2)-eps/5:
            self.control(0, -speed)

            print('Theta =  ' + str(self.theta))
            print('orientation - :  delta = ' + str(alpha - self.theta))
            print('limite inf :  ' + str((np.pi / 2) - eps / 5))
            print('-------------')
        else:
            self.control(speed, 0)
            print('tout droit')
            print('Delta_x =  ' + str(x_target-self.x))
            print('Delta_y =  ' + str(y_target - self.y))
            print('-------------')

    def rejoidre2(self, x_target, y_target, theta_target, eps, p, i, dt):
        alpha = np.arctan2((y_target-self.y), (x_target-self.x))

        if (x_target-eps < self.x < x_target + eps) and (y_target-eps < self.y < y_target + eps):

            if (theta_target-self.theta) > +eps/5:
                if self.mvt != +3:
                    self.controlg.clear()
                    self.controld.clear()
                self.mvt = +3

                self.control2(0, theta_target-self.theta, p, i, dt)

            elif (theta_target-self.theta) < -eps/5:
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
                print('arrêt')

        elif (alpha-self.theta) > (np.pi/2)+eps/5:
            if self.mvt != +1:
                self.controlg.clear()
                self.controld.clear()
            self.mvt=+1

            self.control2(0, alpha-self.theta-(np.pi/2), p, i, dt)


        elif (alpha-self.theta) < (np.pi/2)-eps/5:
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

        UDPSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

        while data != 'exitUDP':
            data, addr = UDPSock.recvfrom(1024) # On s'attend à ce que data soit un string de la forme "cNb1Nb2" où
                                                # 1er lettre : "c" ou "v", c = instruction de coordonnées, v instruction de vitesse
                                                # lettres 2 à 4 est la coordonné en x ou la vitesse de translation
                                                # lettres 5 à 7 est la coordonné en y ou la vitesse de rotation

            if type(data) is str and len(data) == 7:
                return data
