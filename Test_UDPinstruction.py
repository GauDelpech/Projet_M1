from Kabuki import Kabuki
import matplotlib.pyplot as plt
import pygame
import sys

tortue = Kabuki()

ip = 0
port = 0

instruction = tortue.UDPinstruction(ip, port)

if instruction[0] == 'c':
    speed = 10
    dt = 0.1
    tortue.rejoidre(int(instruction[1:3]), int(instruction[4:6]), 0, speed, dt)

    # Ajouter simulation

elif instruction[0] == 'v':
    tortue.control(int(instruction[1:3]), int(instruction[4:6]))

    # Ajouter simulation