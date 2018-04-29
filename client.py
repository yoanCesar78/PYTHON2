# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.messagebox import *
from random import *
import random

import socket,sys, threading

class ThreadReception(threading.Thread):
    """objet thread gÃ©rant la rÃ©ception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        ref_socket[0] = conn
        self.connexion = conn  # rÃ©f. du socket de connexion
              
    def run(self):
        while True:
            try:
                # en attente de rÃ©ception
                message_recu = self.connexion.recv(4096)
                message_recu = message_recu.decode(encoding='UTF-8')
                
                ZoneReception.config(state=NORMAL)
                ZoneReception.insert(END,message_recu)
                # dÃ©filement vers le bas
                ZoneReception.yview_scroll(1,"pages")
                # lecture seule
                ZoneReception.config(state=DISABLED)
                
                if "FIN" in message_recu:
                    global CONNEXION
                    CONNEXION = False
                    
            except socket.error:
                pass
                
def envoyer():
    if CONNEXION == True:
        try:
            message = MESSAGE.get()
            MESSAGE.set("")
            print(message)
            ZoneReception.config(state=NORMAL)
            ZoneReception.insert(END,message+"\n")
            
            # lecture seule
            ZoneReception.config(state=DISABLED)
        
            # Ã©mission 
            ref_socket[0].send(bytes(message,"UTF8"))
            
        except socket.error:
            pass
        


def valider () :
    
    if CONNEXION == True:
        try:
            listrep=[]
            frui=FRUIT.get()
            FRUIT.set("")
            listrep.append(frui)
            ZoneReception.config(state=NORMAL)
            ZoneReception.insert(END,frui)
            ZoneReception.insert(END,"\n")
            # lecture seule
           
            ZoneReception.config(state=DISABLED)
            ref_socket[0].send(bytes(frui,"UTF8"))
            
        except socket.error:
            pass 

def ConnexionServeur():
    

    global CONNEXION

    if CONNEXION == False:
        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            mySocket.connect((HOST.get(), PORT.get()))
            # Dialogue avec le serveur : on lance un thread pour gÃ©rer la rÃ©ception des messages
            th_R = ThreadReception(mySocket)
            th_R.start()
            CONNEXION = True
            ButtonEnvoyer.configure(state = NORMAL)
            ButtonConnexion.configure(state = DISABLED)
            
        except socket.error:
            showerror('Erreur','La connexion au serveur a échouée.')



# état de la connexion
CONNEXION = False

# création ref
ref_socket = {}

# Création de la fenÃªtre principale (main window)
Mafenetre = Tk()

Mafenetre.title('Jeu du Baccalauréat - Interface client ')
Mafenetre.geometry('700x700+50+50')
Mafenetre['bg']='ivory' # couleur de fond

# Frame1 : paramÃ¨tres serveur
Frame1 = Frame(Mafenetre,borderwidth=3,relief=RAISED,bg="white")

Label(Frame1, text = "Adresse IP").grid(row=0,column=0,padx=5,pady=5,sticky=W)
HOST = StringVar()
HOST.set('127.0.0.1')
#Entry(Frame1, textvariable= HOST).grid(row=0,column=1,padx=5,pady=5)

Label(Frame1, text = "Port").grid(row=1,column=0,padx=5,pady=5,sticky=W)
PORT = IntVar()
PORT.set(50026)
#Entry(Frame1, textvariable= PORT).grid(row=1,column=1,padx=5,pady=5)

ButtonConnexion = Button(Frame1, text ='Connexion au serveur',command=ConnexionServeur)
ButtonConnexion.grid(row=0,column=2,rowspan=2,padx=5,pady=5)



Frame1.grid(row=0,column=0,padx=5,pady=5,sticky=W+E)


# Frame 2 : zone de rÃ©ception (zone de texte + scrollbar)
Frame2 = Frame(Mafenetre,borderwidth=2,relief=FLAT,bg="ivory")

# height = 10 <=> 10 lignes
ZoneReception = Text(Frame2,width =60, height =20,state=DISABLED)
ZoneReception.grid(row=0,column=0,padx=5,pady=5)

scroll = Scrollbar(Frame2, command = ZoneReception.yview)

ZoneReception.configure(yscrollcommand = scroll.set)

scroll.grid(row=0,column=1,padx=5,pady=5,sticky=E+S+N)

Frame2.grid(row=1,column=0,padx=5,pady=5)

# Frame 3 : envoi de message au serveur
Frame3 = Frame(Mafenetre,borderwidth=2,relief=RIDGE,bg="white")

MESSAGE = StringVar()
Entry(Frame3, textvariable= MESSAGE).grid(row=0,column=0,padx=5,pady=5)



# les labels

labelUn = Label (Frame3, text="fruit")
labelUn.grid (row = 2,column = 1, sticky = "E", padx = 10)
#labelDeux = Label (Frame3, text="légume:")
#labelDeux.grid (row = 3, column = 1, sticky = "E", padx = 10)
#labelTrois = Label (Frame3, text="pays :")
#labelTrois.grid (row = 4, column = 1, sticky = "E", padx = 10)

labelValider = Label (Frame3, text="") # label de la chaîne de validation
labelValider.grid (row = 4, column = 1, columnspan = 2,\
                   sticky ="W",padx = 10)
# les entrées

FRUIT = StringVar()
entreeUn = Entry (Frame3,textvariable=FRUIT)
entreeUn.grid (row = 2, column = 2)
entreeUn.focus_set()

#entreeDeux = Entry (Frame3)
#entreeDeux.grid (row = 3, column = 2)

#entreeTrois = Entry (Frame3)
#entreeTrois.grid (row = 4, column = 2)


ButtonEnvoyer = Button(Frame3, text ='Envoyer', command = envoyer)
ButtonEnvoyer.grid(row=0,column=1,pady=10)



ButtonEnvoyer2 = Button(Frame3, text ='Valider sa réponse', command = valider)
ButtonEnvoyer2.grid(row=5,column=5,padx=5,pady=5)

BoutonQuitter = Button(Frame3, text ='Quitter', command = Mafenetre.destroy)
BoutonQuitter.grid(row=0,column=55,padx=55,pady=5)

Frame3.grid(row=2,column=0,padx=5,pady=5,sticky=W+E)

Mafenetre.mainloop()
