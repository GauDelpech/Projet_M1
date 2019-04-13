from Kabuki import Kabuki
import matplotlib.pyplot as plt

tortue = Kabuki()

ip = 0
port = 0
instruction = 'none'

while instruction != 'exitUDP':
    instruction = tortue.UDPinstruction(ip, port)

    if instruction[0] == 'c':
        eps = 0.1
        tortue.rejoidre(int(instruction[1:3]), int(instruction[4:6]), 0, eps)


        i = 0
        pas = 0.1

        while i <= 1000:
            tortue.new_pos(pas)
            i += pas

        plt.plot(tortue.histx, tortue.histy)
        plt.title('Trajectoire du robot pour rejoindre la position (' + str(instruction[1:3]) + ', ' + str(instruction[4:6]) + ')')
        plt.show()


    elif instruction[0] == 'v':

        tortue.control(int(instruction[1:3]), int(instruction[4:6]))

        i=0
        pas = 0.1

        while i <= 1000:
            tortue.new_pos(pas)
            i += pas

        plt.plot(tortue.histx, tortue.histy)
        plt.title('Trajectoire du robot pour vtrans =' + str(instruction[1:3]) + ' et vrot = ' +  str(instruction[4:6]))
        plt.show()