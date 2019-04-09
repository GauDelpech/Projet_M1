from Moteur import MoteurCC
import matplotlib.pyplot as plt

moteur = MoteurCC()
moteur0 = MoteurCC(l=0)


ttot = 1
pas = 0.01

# moteur.rep_ind(0, pas, ttot)

t = 0
temps = [t]
omega = 0
ome = [omega]
omega0 = 0
ome0 = [omega0]

while t <= ttot:
    um = 1
    omega = moteur.volt_to_speed(um, omega, pas)
    ome.append(omega)
    omega0 = moteur.volt_to_speed(um, omega0, pas)
    ome0.append(omega0)

    t += pas
    temps.append(t)

plt.plot(temps, ome, 'b', label='Avec inductance')
plt.plot(temps, ome0, 'r', label='Sans inductance')
plt.legend()
plt.title('Simulation numérique du moteur à courant continu (pas de ' + str(pas) +')')
plt.xlabel("temps (s)")
plt.ylabel("Vitesse de rotation (rad/s)")
plt.show()