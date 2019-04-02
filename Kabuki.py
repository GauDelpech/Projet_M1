import numpy as np
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

        self.rayon = 1.5  # 37.5
        self.ecart = 14.06  # 351.5

        self.histx = [x]
        self.histy = [y]

        self.color = color

    def set_pos(self, x, y, theta):
        self.x = x
        self.y = y
        self.theta = theta

    def get_pos(self):
        return [self.x, self.y, self.theta]

    def set_speed(self, vg, vd):
        self.vg = vg
        self.vd = vd

        self.v = (self.rayon / 1)*(self.vd + self.vg)
        self.vtheta = (self.rayon/self.ecart)*(self.vd-self.vg)

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

        self.vg = (eps_r - self.ecart*eps_t)/self.rayon
        self.vd = (eps_r + self.ecart*eps_t)/self.rayon


    def rejoidre(self, x_target, y_target, theta_target, speed, dt):
        alpha = np.arctan2((x_target-self.x), (y_target-self.y))

        if (alpha-self.theta) >= 0:
            while self.theta != alpha:
                self.control(0, speed)
                self.new_pos(dt)
        else:
            while self.theta != alpha:
                self.control(0, -speed)
                self.new_pos(dt)

        while self.x != x_target and self.y != y_target:
            self.control(speed,0)
            self.new_pos(dt)

        if (theta_target-self.theta) >= 0:
            while self.theta != theta_target:
                self.control(0, speed)
                self.new_pos(dt)
        else:
            while self.theta != theta_target:
                self.control(0, -speed)
                self.new_pos(dt)

        self.set_speed(0, 0)
        self.new_pos(dt)
