import numpy as np
import matplotlib.pyplot as plt
import sys


class MoteurCC(object):

    def __init__(self, r=1, l=0.001, kc=0.01, ke=0.01, j=0.01, f=0.1):
        self.r = r
        self.l = l
        self.kc = kc
        self.ke = ke
        self.j = j
        self.f = f

        self.i = []
        self.v = []
        self.dt = []

    def volt_to_speed(self, um, omega, dt):
        i = (um - self.ke * omega)/self.r
        gamma = self.kc*i
        d_omega = (gamma-self.f*omega)/self.j
        return (dt*d_omega+omega)

    def volt_to_speed2(self, um, omega, dt):
        if um > 12:
            um = 12
        elif um < -12:
            um = -12

        i = (um - self.ke * omega)/self.r

        if i > 0.750:
            i = 0.750
        elif i < -0.750:
            i = -0.750

        gamma = self.kc*i
        d_omega = (gamma-self.f*omega)/self.j
        new_omega = (dt*d_omega+omega)

        if new_omega > (8800*(2*np.pi/60)):
            new_omega = (8800 * (2 * np.pi / 60))
        elif new_omega < -(8800 * (2 * np.pi / 60)):
            new_omega = -(8800 * (2 * np.pi / 60))

        self.i.append(i)
        self.v.append(um)
        self.dt.append(dt)

        return new_omega

    def anal_speed(self, um, t):
        omega = (1-np.exp((-1/self.j)*(self.f+(self.kc*self.ke/self.r))*t))*(self.kc*um/(self.r*self.f+self.kc*self.ke))
        return omega

    def rep_ind(self, omega_init, dt, temps_tot):
        um = 1
        t=0
        temps = [t]
        ome_num = [omega_init]
        ome_ana = [omega_init]
        ome=omega_init

        while t <= temps_tot:

            ome = self.volt_to_speed(um, ome, dt)
            ome_num.append(ome)

            ome_ana.append(self.anal_speed(um, t))

            t += dt
            temps.append(t)

        plt.plot(temps, ome_ana, 'b')
        plt.plot(temps, ome_num, 'r')
        plt.title("Vitesse de rotation calculée analytiquement (bleu) et numériquement (rouge)")
        plt.xlabel("temps (s)")
        plt.ylabel("Vitesse de rotation (rad/s)")
        plt.show()

    def conso(self):
        p = 0
        t = 0
        batterie = 2.2
        for k in range(len(self.i)):
            p += self.i[k]*self.v[k]
            t += self.dt[k]
            batterie -= self.i[k]

        batterie = (batterie*100)/2.2

        return [p, t, batterie]


class Controleur(object):

    def __init__(self, vitesse_desiree=0, vitesse_actuelle=0):
        self.va = vitesse_actuelle
        self.vd = vitesse_desiree
        self.esp = self.vd-self.va

    def prop(self, p):
        return p*(self.vd-self.va)

    def pi(self, p, i, dt):
        if i <= 0.00000001:
            sys.exit('erreur i = 0')

        prop = self.vd - self.va

        self.esp += (self.vd - self.va)
        inte = (dt/i)*self.esp

        return p*(prop + inte)

    def clear(self):
        self.esp = 0
