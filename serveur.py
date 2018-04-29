# -*- coding: utf-8 -*-

import socket, sys, threading, time
from random import *
import random

# variables globales

# adresse IP et port utilisÃ©s par le serveur
HOST = ""
PORT = 50026

NOMBREJOUEUR = int(input("choisissez le nombre de joueur :"))
dureemax = 15 # durÃ©e max question ; en secondes
pause = 3 # pause entre deux questions  ; en secondes
timefin=100

dict_clients = {}  # dictionnaire des connexions clients
dict_pseudos = {}  # dictionnaire des pseudos
dict_reponses = {}  # dictionnaire des rÃ©ponses des clients
dict_scores = {} # dictionnaire des scores de la derniÃ¨re question
dict_scores_total = {}

# liste des questions

lf=['Abricot','Airelle','Aki','Ananas','Arbouse','Avocat','Banane','Barbadine','Bigarade','Brugnon','Cabosse','Carambole','Cassis','Cédrat','Cériman','Cerise','Châtaigne','Chayote','Citron','Clémentine','Clemenvilla','Coing','Combava','Corme','Cranberry','Curuba','Datte','Feijoas','Figue','Fraise','Framboise','Fruit de la passion','Girembelle','Goyave','Grenade','Grenadelle','Grenadille','Griotte','Groseille','Icaque','Jaboticaba','Jambolan','Jaque','Jujube','Kaki','Kiwaï','Kiwi','Kumquat','Lime','Litchi','Longane','Mandarine','Mangoustan','Mangue','Marang','Marron','Melon','Mirabelle','Mûre','Myrtille','Nectarine','Nèfle','Noisette','Noix','Noix de coco','Olive','Orange','Pamplemousse','Papaye','Pastèque','Pêche','Physalis','Pistache','Pitaya','Poire','Pomelo','Pomme','Prune','Pruneau','Prunelle','Quetsche','Raisin','Ramboutan','Sapote','Tamarin','Tangerine','Tomate','Yuzu','Zévi']
lettres=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R']

list_lettre = []
tour=3
for i in range(0,tour):
    lAlea=random.choice(lettres)
    list_lettre.append((lAlea))


class ThreadClient(threading.Thread):
    '''dÃ©rivation de classe pour gÃ©rer la connexion avec un client'''
    
    def __init__(self,conn):

        threading.Thread.__init__(self)
        self.connexion = conn
        
        # MÃ©moriser la connexion dans le dictionnaire
        
        self.nom = self.getName() # identifiant du thread "<Thread-N>"
        dict_clients[self.nom] = self.connexion
        dict_scores[self.nom] = 0
        dict_scores_total[self.nom] = 0
        
        print("Connexion du client", self.connexion.getpeername(),self.nom ,self.connexion)
        
        message = bytes("Vous etes connecté au serveur.\n","utf-8")
        self.connexion.send(message)
        
        
    def run(self):
        
        # Choix du pseudo    
        
        self.connexion.send(b"Entrer un pseudo :\n")
        # attente rÃ©ponse client
        pseudo = self.connexion.recv(4096)
        pseudo = pseudo.decode(encoding='UTF-8')
        dict_pseudos[self.nom] = pseudo
        print("Pseudo du client", self.connexion.getpeername(),">", pseudo)
        
        message = b"Attente des autres clients...\n"
        self.connexion.send(message)
    
        # RÃ©ponse aux questions
       
        while True:
            
            try:
                # attente rÃ©ponse client
                reponse = self.connexion.recv(4096)
                reponse = reponse.decode(encoding='UTF-8')
            except:
                # fin du thread
                break
                
            # on enregistre la premiÃ¨re rÃ©ponse
            # les suivantes sont ignorÃ©es
            if self.nom not in dict_reponses:
                dict_reponses[self.nom] = reponse, time.time()
                print("reponse du client ",self.nom,">",reponse)

        print("\nFin du thread",self.nom)
        self.connexion.close()

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