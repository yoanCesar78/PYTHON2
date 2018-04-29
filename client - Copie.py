import random
import socket
import struct
import sys
import time


def throw(N):
  in_circle = 0;
  for i in range(N):
    x = random.random()
    y = random.random()
    if x*x + y*y <= 1:
      in_circle += 1
  return in_circle

# Cree un packet de donnee a partir des deux valeurs entieres v1 et v2 passees
# en parametre. C'est la serialisation et ce sera l'objet de cour 4.
def CreatePacket(v1, v2):
  return struct.pack("!II", v1, v2)

# Ouvre et retourne une socket en mode connecte a l'adrresse et sur le port
# passes en parametre.
def CreateSocket():
  # La socket doit etre ouverte avec la famille d'adressage par defaut et le
  # protocol UDP (socket de type datagram)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  return sock

if __name__ == "__main__":
  
  packet_sent = 0
  # Ouvrir la socket
  sock = CreateSocket()
  
  # Recuprer les parametres de lance depuis la ligne de commande
  M = int(sys.argv[1])
  N = int(sys.argv[2])
  
  i = 0
  while i < M:
    in_circle = throw(N)
    packet = CreatePacket(in_circle, N)
    sock.sendto(packet, ("127.0.0.1", 12345))
    packet_sent += 1
    i += 1

  print "Sent " + str(packet_sent) + " packets."
  # Fermer la socket 
  sock.close()