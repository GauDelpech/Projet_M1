import numpy as np

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

        self.v = (self.rayon / 2)*(self.vd + self.vg)
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


