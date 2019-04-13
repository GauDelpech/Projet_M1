from Moteur import MoteurCC
from Moteur import Controleur
import matplotlib.pyplot as plt

def Simul_prop(moteur=MoteurCC(), control=Controleur(), p=10, pas=0.1, ttot=2):

    t = 0
    temps = [t]
    omega = 0
    ome = [omega]
    val_des = [control.vd]

    while t <= ttot:
        um = control.prop(p)
        omega = moteur.volt_to_speed(um, omega, pas)
        ome.append(omega)

        control = Controleur(control.vd, omega)
        t += pas
        temps.append(t)
        val_des.append(control.vd)


    plt.plot(temps, val_des, 'r', label='Valeur cible')
    plt.plot(temps, ome, 'b', label='Vitesse moteur')
    plt.legend()
    plt.title('Correction proportionnelle (P='+str(p)+ ') de la vitesse du moteur (pas de ' + str(pas)+ ')')
    plt.xlabel("temps (s)")
    plt.ylabel("Vitesse de rotation (rad/s)")
    plt.show()

def Simul_pi(moteur=MoteurCC(), control=Controleur(), p=10, i=1, pas=0.1, ttot=2):

    t = 0
    temps = [t]
    omega = 0
    ome = [omega]
    val_des = [control.vd]

    while t <= ttot:
        um = control.pi(p, i, pas)
        omega = moteur.volt_to_speed(um, omega, dt)
        ome.append(omega)

        control.va = omega
        t += pas
        temps.append(t)
        val_des.append(control.vd)

    plt.plot(temps, val_des, 'r', label='Valeur cible')
    plt.plot(temps, ome, 'b', label='Vitesse moteur')
    plt.legend()
    plt.title('Correction PI (P='+str(p)+ ' et I='+str(i)+') de la vitesse du moteur (pas de ' + str(pas)+ ')')
    plt.xlabel("temps (s)")
    plt.ylabel("Vitesse de rotation (rad/s)")
    plt.show()

    control.clear()


moteur = MoteurCC()
contr = Controleur(10)

P = 500
I = 0.1
dt = 0.000001
ttot = 0.025

Simul_prop(moteur, contr, P, dt, ttot)
Simul_pi(moteur, contr, P, I, dt, ttot)


