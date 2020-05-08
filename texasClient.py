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
                # print(str(i)+suit)
        
        
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
        
    # def print_status(self):
    #     print("------------------------------\n")
    #     print("Betting round: " + str(self.bet_round))
    #     print("Current pot: $"+str(self.pot))
    #     print("Public hand: "+str(self.public_cards))
    #     print("Players (in betting order): ")
    #     print([player.pid for player in self.player_list])
    #     print("Player accounts:")
    #     print([player.current_balance_server for player in self.player_list])
    #     print(self.player_list.__getitem__(self.curr_player_idx))
        
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
def handle(incoming_buffer, ipServer): # not used
    while True:
        # incoming_buffer definition: list for saving incoming messages      
        if len(incoming_buffer)>0:            
            s = incoming_buffer.pop()
            info = s.split(' ')
            selfID = info[len(info)-2]
            ip = info[len(info)-1]
            if(ip == ipServer and selfID == ID):
                if(s.startswith("create")):                   
                    roomID = info[1]
                    print("create successfully and the room ID is "+roomID)
                if(s.startswith("start")):                   
                    roomID = info[1]
                    print("start successfully and the room ID is "+roomID)
                if(s.startswith("join")):                   
                    roomID = info[1]
                    print("join successfully and the room ID is "+roomID)
                else:
                    info = s.split(' ')
                    selfID = info[len(info)-1]
                    ip = info[len(info)-2]
                    if(selfID == ID and ip == ipServer):                
                        print("failed to join the game because of " + s)
            
                
            
def listen(ip, port, incoming_buffer): # listen the feedback from the server and appends to incoming_buffer
    #print("Server is starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip: is the local ip address
    ip = '192.168.2.2'
    sock.bind((ip, port))
    sock.listen(5)
    #print("Server is listenting port 8001, with max connection 5")
    # Isaac moved the next two lines out of the while loop
    
    while True:
        connection, address = sock.accept()
        try:
            connection.settimeout(10000)
            buf = connection.recv(1024)
            s = buf.decode("utf-8")
            
            sfull = s+" "+address[0]
            print(s)
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

def play(incoming_buffer):
    while True:  
            time.sleep(0.05)
            if len(incoming_buffer)>0:            
                s = incoming_buffer.pop()
                info = s.split(' ')
                selfID = info[len(info)-2]
                ip = info[len(info)-1]

                if(ip == ipServer and int(selfID) == ID):  #check whether the sender is the Server and send to our ID
                    if(s.startswith('first')):                                
                            print("your card in hand: " + info[len(info)-4])
                            bet = input("do you want to start the bet? y or n: ") # means you are the fisrt one to bet
                            if(bet == 'y'):
                                amount = input("how much do you want to bet?")# how many chip_amounts do you want to bet
                                print("you have "+info[len(info)-3]+" chip_amount")
                                print("your card in hand is "+info[len(info)-4])
                                while(int(amount)>int(info[len(info)-3]) or int(amount) == 0):# you bet amount should be less than the chip_amounts you have
                                    amount = input("you do not have enough money or you input no money, reinput it: ")
                                mess = "bet-start "+amount+" "+roomID+" "+name
                                send(ipServer,port, mess)
                            else:
                                mess = 'n '+roomID+" "+name
                                send(ipServer,port, mess)
                                           
                    if(s.startswith('over')):
                        print('gameOver')
                        sys.exit()
                    if(s.startswith('name') or s.startswith('chip_amount') or s.startswith('card')):
                        print(info[0])
                    
                    if(s.startswith('the-bet')):#Previously, there is someone bet, do you want to follow him
                        print("do you want to follow the bet? the bet amount is "+info[len(info)-3])
                        print("you have "+info[len(info)-4]+" chip_amount")
                        print("your card in hand is "+info[len(info)-5 ])
                        bet = input(" y or n: ")
                        if(bet == 'y'):
                            if(info[len(info)-3] > info[len(info)-4]):# if you do not have enough chip_amounts, and you choose yes, just show hand 
                                amount = int(info[len(info)-4])
                            else:
                                amount = int(info[len(info)-3])
                            mess = "bet-start "+str(amount)+" "+roomID+" "+name
                            send(ipServer,port, mess)
                    if(s.startswith('Game end') or s.startswith("Player") or s.startswith("3") or s.startswith("4") or s.startswith("5")):#this is to check whether this round of game is end, or does the player bet or not ,or who is the winner of the game
                        '''info = s.split(' ')
                        info = info[0:len(info)-2]
                        print(" ".join(info))'''
                        print(s)
                                    
                    elif(s.startswith("fail")):
                        print("fail to start")
                        sys.exit()

#code starts to run
#name = input("Enter your name : ") #input yout own name
name = 'boyang'
print("Your name is "+name)
      
#chip_amount = input("Enter your chip_amount : ") # input your chip_amount which is used to bet
chip_amount = '100'
print("your chip_amount is "+chip_amount)
#ipServer = input("ip address of the texasSever : ") # ipAddress of the server, the client can only send message to the server and receive the message from the server
ipServer = '192.168.2.3'
print("your server IP address is "+ipServer)
# ip is a placeholder
ip = '127.0.0.1'
port = 8001
t1 = threading.Thread(target=listen,args=(ip, port, incoming_buffer))#create one thread keep listening from the server, all the information receiverd is added to list incoming_buffer - only deal with one message at a time
t1.start()

create_game_yn = input("do you want you create game? please use y or n : ") #whether you want to create a room for game or not
if create_game_yn == 'y':
    createGame(ipServer,port, name,ID,chip_amount) #send create request to the server
    # what is this while true for? 
    while True:   
        if len(incoming_buffer)>0:            
            s = incoming_buffer.pop()
            info = s.split(' ')
            selfID = info[len(info)-2]
            ip = info[len(info)-1]
            if(ip == ipServer and int(selfID) == ID): # since each machine can be server clients with different id, so the client only deal with feedback from the server with its own id
                if(s.startswith("create")):                   
                    roomID = info[1]
                    print("create successfully and the room ID is "+roomID)#create successfully and get the roomID, this client is the owner of the game
                    break
                else:
                    print('wrong')
    
    start_game_yn = input("do you want to start the game? use y or n : ")
    if start_game_yn == "y":
        startGame(ipServer,port,name,ID,chip_amount, roomID) #send start request to the server
        play(incoming_buffer)
                        
    
else:
    joing_game_yn = input("do you want you join game? please use y or n : ") # whether to join a game whose owner is anothet client
    if joing_game_yn == 'y':
        roomID = input("roomID is : ")                  #if you want to join the name, you need to know the roomID from the gameOwner
        joinGame(ipServer,port,name,ID, chip_amount, roomID)  
        while True:   
            if len(incoming_buffer)>0:            
                s = incoming_buffer.pop()
                # Isaac: the thing that is being split is the incoming message.
                info = s.split(' ')
                selfID = info[len(info)-2]
                ip = info[len(info)-1]
                if(ip == ipServer and int(selfID) == ID):
                    if(s.startswith("join")):                   
                        roomID = info[1]
                        print("join successfully and the room ID is "+roomID)
                if(s.startswith("start")):                   #if received start, means we sucessfully start the game
                        print("start successfully and the room ID is "+roomID)     
                        play(incoming_buffer)
#t3 = threading.Thread(target=start,)
#t3.start()