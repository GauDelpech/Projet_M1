import numpy as np


class MoteurCC(object):

    def __init__(self, r=1, l=0.001, kc=0.01, ke=0.01, j=0.01, f=0.1):
        self.r = r
        self.l = l
        self.kc = kc
        self.ke = ke
        self.j = j
        self.f = f

    def volttospeed (self, um, omega, dt):
        i=(um - self.ke * omega)/self.r
        gamma=self.kc*i
        d_omega=(gamma-self.f*omega)/self.j
        return (dt*d_omega+omega)

    def analspeed(self, dt, ttot):
        t=0
        omegaTot = []

        while t <= ttot:
            omega = (1- numpy.exp() )
            t += dt
            omegaTot.append(omega)
