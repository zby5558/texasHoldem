#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 19:29:22 2020

@author: boyang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:44:28 2020

@author: boyang 
"""
import threading
import socket   
import random
import netifaces as ni
import time
import sys
import numpy as np
import random

class deck_cards:
    deck = []
    flaglist = []
    def __init__(self):
        deck = []
        for suit in [' of SPADES',' of CLUBS',' of HEARTS',' of DIAMONDS']:    
            for i in ['2','3','4','5','6','7','8','9','10','J','Q','K','A']:
                self.deck.append(str(i)+suit)
                self.flaglist.append(1)
                # #print(str(i)+suit)
        
        
    def print_cards(self):
        for i in range(len(self.deck)):
            if self.flaglist[i]==1:
                print(self.deck[i])
    

class player:
    def __init__(self, pid, personal_hand, starting_balance, is_creator):
        self.pid = pid
        self.is_creator = is_creator
        self.personal_hand = personal_hand
        self.starting_balance = starting_balance
        self.current_balance_server = starting_balance
        self.myturn = False
        self.winner = False
        self.status = "Active" # might otherwise be folded
        
    def __str__(self):
        return str(self.pid)+"("+self.status+", has $"+str(self.current_balance_server)+")"
    
class pokerTable:
    def __init__(self, first_player,game_id):
        self.game_id = game_id
        self.deck = deck_cards()
        self.bet_round = 0
        self.game_started = False # aka bet_round is zero
        self.pot = 0
        self.public_cards = ['X','X','X','X','X']
        self.player_list = []
        self.curr_player_idx = 0
        self.first_player = first_player
        
        
    def add_player(self, new_player, game_id):
        if not self.game_started:
            self.player_list.append(new_player)
        
    def whos_turn(self):
        return self.curr_player_idx
        
    # def #print_status(self):
    #     #print("------------------------------\n")
    #     #print("Betting round: " + str(self.bet_round))
    #     #print("Current pot: $"+str(self.pot))
    #     #print("Public hand: "+str(self.public_cards))
    #     #print("Players (in betting order): ")
    #     #print([player.pid for player in self.player_list])
    #     #print("Player accounts:")
    #     #print([player.current_balance_server for player in self.player_list])
    #     #print(self.player_list.__getitem__(self.curr_player_idx))
        
    def __str__(self):
        return "------------------------------------------------------------------"+\
            "\nGame id: "+str(self.game_id)+", Pot size: $"+str(self.pot)+", Betting round: "+str(self.bet_round)+ \
            "\nPlayers (betting order):"+\
            "\n"+" // ".join(str(x) for x in self.player_list)+\
            "\nCards: ["+" ".join(str(x) for x in self.public_cards)+"]"\
            "\nPot: $"+str(self.pot)+\
            "\n"+str(self.player_list[self.curr_player_idx])+'\'s turn to bet...'

incoming_buffer = []
roomID = '1'
ID = random.randint(1,10000) #since we do not have enough machine, each machine can be used as several clients. Thus ID is used to distingush different players in one machine(haven't be implemented yet)
timer = np.zeros(1000)
       
                
            
def listen(ip, port, incoming_buffer): # listen the feedback from the server and appends to incoming_buffer
    ##print("Server is starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip: is the local ip address
    ip = '192.168.1.14'
    sock.bind((ip, port))
    sock.listen(5)
    ##print("Server is listenting port 8001, with max connection 5")
    # Isaac moved the next two lines out of the while loop
    
    while True:
        connection, address = sock.accept()
        try:
            connection.settimeout(10000)
            buf = connection.recv(1024)
            s = buf.decode("utf-8")
            #print(s)
            sfull = s+" "+address[0]
            incoming_buffer.append(sfull)
        except socket.timeout:
            print('time out')
def send(ip,port,mess):  #send function is used to send message to the taxasSever
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((ip, port))
    byt = mess.encode()
    sock.send(byt)
def createGame(ip,port,name,ID, chip_amount):
    mess = "create "+name+" "+str(ID)+" "+str(chip_amount)
    send(ip, port, mess)
def joinGame(ip,port,name,ID, chip_amount, roomID):
    mess = "join "+name+" "+str(ID)+" "+chip_amount+" "+str(roomID)
    send(ip, port, mess)
def startGame(ip,port,name,ID, chip_amount, roomID):
    mess = "start "+name+" "+str(ID)+" "+chip_amount+" "+str(roomID)
    send(ip, port, mess)

def play(incoming_buffer):#auto reply to all the messages come from the server
    while True:  
            time.sleep(0.05)
            if len(incoming_buffer)>0:            
                s = incoming_buffer.pop()
                info = s.split(' ')
                selfID = int(info[len(info)-2])
                ip = info[len(info)-1]
                timer[selfID] = time.time()#record the time when the player selfID receives the message
                rID = info[1]

                if(ip == ipServer):  #check whether the sender is the Server and send to our ID
                    if(s.startswith('first')):                                
                        amount = random.randint(1,5)
                        '''while(int(amount)>int(info[len(info)-3]) or int(amount) == 0):# you bet amount should be less than the chip_amounts you have
                            amount = input("you do not have enough money or you input no money, reinput it: ")'''
                        mess = "bet-start "+str(amount)+" "+rID+" "+str(selfID)
                        send(ipServer,port, mess)

                                           
                    if(s.startswith('over')):
                        #print('gameOver')
                        sys.exit()
                   
                    
                    if(s.startswith('the-bet')):#Previously, there is someone bet, do you want to follow him                      
                            if(info[len(info)-3] > info[len(info)-4]):# if you do not have enough chip_amounts, and you choose yes, just show hand 
                                amount = int(info[len(info)-4])
                            mess = "bet-start "+str(amount)+" "+rID+" "+str(selfID)
                            send(ipServer,port, mess)                                
                    elif(s.startswith("fail")):
                        #print("fail to start")
                        sys.exit()
def check():#iteratively check 1000 players for 100 virtual table, check whether the interval between two consequtive messages received by one player is larger than 5s.
   
    count = 0
    while True:
        count = count+1
        k = 0
        time.sleep(3)
        cur = time.time()
        for i in range(1,1000): # 1000 players only works for 100 virtual tables in the server side. If there are k tables in the server side, you can modify it to "for i in range(1,10*k)" where k is the # of tables you have in the TestServer function in TexasTestServer.py
            if(count < 2):
                if(cur-timer[i] > 5 and timer[i] != 0):
                    k = k+1
            else:
                if(cur-timer[i]>5):
                    k = k+1
        print(k)
            
#code starts to run
#name = input("Enter your name : ") #input yout own name
name = 'boyang'
#print("Your name is "+name)
      
#chip_amount = input("Enter your chip_amount : ") # input your chip_amount which is used to bet
chip_amount = '100'
#print("your chip_amount is "+chip_amount)
#ipServer = input("ip address of the texasSever : ") # ipAddress of the server, the client can only send message to the server and receive the message from the server
ipServer = '192.168.1.17'
#print("your server IP address is "+ipServer)
# ip is a placeholder
ip = ''
port = 8001
t1 = threading.Thread(target=listen,args=(ip, port, incoming_buffer))#create one thread keep listening from the server, all the information receiverd is added to list incoming_buffer - only deal with one message at a time
t1.start()

t3 = threading.Thread(target=check,)#create one thread keep listening from the server, all the information receiverd is added to list incoming_buffer - only deal with one message at a time
t3.start()
play(incoming_buffer)