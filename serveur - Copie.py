import random
import socket
import struct
import sys
from threading import Thread
import time

MAX_BUFFER = 1024

packet_queue = []

# Thread charger de gerer l'arrive des paquets de la socket passee en parametre.
# Extrait les donnees du paquet et les stocke dans une file en attente d'etre
# traitees.
class HandlePacket(Thread):
  def __init__(self, sock):
    Thread.__init__(self)
    self.sock = sock

  def run (self):
    while True:
      packet, addr = self.sock.recvfrom(MAX_BUFFER)
      packet_queue.append(ProcessPacket(packet))


# Extrait deux entiers du paquet passe en parametre et les retourn dans un
# couple.
def ProcessPacket(packet):
  return struct.unpack("!II", packet)

# Ouvre et retourne une socket en mode ecoute sur l'adrresse et le port
# passes en parametre.
def CreateSocket(address, port):
  # La socket doit etre ouverte avec la famille d'adressage par defaut et le
  # protocol UDP (socket de type datagram)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  print sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
#  sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
  print sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
  sock.bind((address, port))

  return sock


if __name__ == "__main__":

  total_in_circle = 0.0
  count_throw = 0.0
  current_pi = 0.0
  packet_received = 0

  # Ouvrir la socket
  sock = CreateSocket("127.0.0.1", 12345)
  
  # Creer un thread pour gerer les arrivees de paquets.
  thread = HandlePacket(sock)
  thread.start()

  # Attendre les valeurs envoyees par les clients et mettre a jour la valeur
  # courrante de pi.
  while True:
#    packet, addr = sock.recvfrom(MAX_BUFFER)
    while len(packet_queue):
      (in_circle, throw) = packet_queue.pop()
      packet_received += 1
#      (in_circle, throw) = ProcessPacket(packet)
      total_in_circle += in_circle
      count_throw += throw
      current_pi = total_in_circle * 4 / count_throw
     
    print "Current Pi approximation :\t" + (str(current_pi) + "(" +
        str(count_throw) + ")\t/\tReceived " + str(packet_received) + 
        " packets")
    time.sleep(2)
  
#  thread.join()
  # Fermer la socket 
  sock.close()