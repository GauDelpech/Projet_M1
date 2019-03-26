import numpy as np
import matplotlib.pyplot as plt

class MoteurCC(object):

    def __init__(self, r=1, l=0.001, kc=0.01, ke=0.01, j=0.01, f=0.1):
        self.r = r
        self.l = l
        self.kc = kc
        self.ke = ke
        self.j = j
        self.f = f

    def volt_to_speed (self, um, omega, dt):
        i=(um - self.ke * omega)/self.r
        gamma=self.kc*i
        d_omega=(gamma-self.f*omega)/self.j
        return (dt*d_omega+omega)

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

            ome = moteur.volt_to_speed(um, ome, dt)
            ome_num.append(ome)

            ome_ana.append(moteur.anal_speed(um, t))

            t += dt
            temps.append(t)

        plt.plot(temps, ome_ana, 'b')
        plt.plot(temps, ome_num, 'r')
        plt.title("Vitesse de rotation calculée analytiquement (bleu) et numériquement (rouge)")
        plt.xlabel("temps (s)")
        plt.ylabel("Vitesse de rotation (rad/s)")
        plt.show()

class Controleur(object):

    def __init__(self, vitesse_desiree=0, vitesse_actuelle=0):
        self.va = vitesse_actuelle
        self.vd = vitesse_desiree

    def prop(self, p):
        eps = self.vd-self.va
        return p*eps


moteur = MoteurCC()
p = Controleur(10)

t = 0
dt = 0.01
ttot = 2
omega = 0
ome = [omega]
temps = [t]

while t <= ttot:
    um = p.prop(150)
    omega = moteur.volt_to_speed(um, omega, dt)
    ome.append(omega)

    p = Controleur(8, omega)
    t += dt
    temps.append(t)

plt.plot(temps, ome)
plt.show()