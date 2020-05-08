#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:41:31 2020

@author: boyang
"""
import threading
import socket        
import random  
import time
import netifaces as ni

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



roomID = 0      # the roomID of the game
gamerName = []  #the name of each gamer in the game
gamerID = []    #ID of each gamer in the game
fiveCards = []  # three cards which can be shared by all plyaers. The name is wrong 
cardInHand = []  # The card owned by each gamer
gameOwner = []  # the name of the game owner
gamerIP = []    # the IP address of each gamer
gamerChip = []  # the chip of each gamer
cardLeft = []   # card left in the game after drawing 
gamerLeft = []  # whether a gamer bet or not in the game
start = []      # whether the game is start or not
RANKS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] # rank of cards
SUITS = ['S', 'D', 'H', 'C'] # suits of cards
cards = []  # 52 cards
chipAmount = [] # if a player wins, the amound of chips he or she can win. For example, if each player bet 50 chips and there are 5 players, the chipAmount for this game is 50*5 = 250
betStart = []  # whether the person is the first one to bet
currentChip = [] # if you are not the first one to bet, currentChip shows the how much you should bet
gamerReply = [] # whether each gamer replies to bet or not
for i in range(0,13):
    for j in range(0,4):
        cards.append(str(RANKS[i])+SUITS[j]) # cards contain 52 cards

for i in range(0,100):      # in this program, there are more than one game that can be held by the server. The maximum number of game is 100. For example, gamerName[rID] is the name list of gamers in the room number rID. 
    chipAmount.append(0)
    currentChip.append(0)
    betStart.append(0)
    gamerName.append([])
    gamerReply.append([])
    gamerID.append([])
    gamerIP.append([])
    gamerChip.append([])
    fiveCards.append([])
    cardInHand.append([])
    gameOwner.append('')
    gamerLeft.append([])
    cardLeft.append([])
    start.append(0)
def send(ip,port,mess): #send message to the clients
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((ip, port))
    byt = mess.encode()
    sock.send(byt) 
def getcreate(s): 
    info = s.split(" ")
    name = info[1]
    ID = info[2]
    chip = info[3]
    ip = info[4]
    return name,ID,chip,ip
def getjoin(s):
    info = s.split(" ")
    name = info[1]
    ID = info[2]
    chip = info[3]
    rID = int(info[4])
    ip = info[5]
    return name,ID,chip, rID, ip
def broadcast(rID,gamerID,gamerIP,s): #broadcast the message to all the clients in the game which has a roomID rID
    for i in range(0,len(gamerID[rID])):
        if(gamerID[rID][i].startswith('virtual')):
            continue
        ID = gamerID[rID][i]
        ip = gamerIP[rID][i]
        mess = s+" "+str(rID)+" "+ID
        send(ip,port,mess)
def updateInfo(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft):# broadcast the name, chip owned by each gamer and the first two cards of each gamer. And the gamer will also get the cards he has which are not shown to others
    namestr = 'name'
    chipstr = 'chip'
    cardstr = 'card'
    for i in range(0,len(gamerName[rID])):
        namestr = namestr+'-'+gamerName[rID][i]
        chipstr = chipstr+'-'+str(gamerChip[rID][i])
        cardstr = cardstr+'-'+str(','.join(cardInhand[rID][i]))
    for i in range(0,len(gamerID[rID])):
        if(gamerID[rID][i].startswith('virtual')):
            continue
        ID = gamerID[rID][i]
        ip = gamerIP[rID][i]
        
        mess = namestr+' '+str(rID)+" "+ID
        mess1 = chipstr+' '+str(rID)+" "+ID
        mess2 = cardstr+' '+str(rID)+' '+ID
        print("ip "+ip)
        send(ip,port,mess)
        send(ip,port,mess1)
        send(ip,port,mess2)

def bet(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft):# check whether each gamer bet or not
    print("start bet")
    numPlayers = 0 # how many players bet
    lastPlayer = 0 # the last player bet
    print(gamerName[rID])
    for i in range(len(gamerName[rID])):
        if(gamerLeft[rID][i] == 1 or gamerChip[rID][i] == 0):#if the player left the game, gamerLeft[rID][i] == 1, the player cannot bet. Player with 0 chip cannot bet.
            continue
        
        while(i != 0 and gamerReply[rID][i-1] == 0):  # if a player has already replied, gamerReplay[rID][i] should be one. this part is to wait until your previous player replies
            time.sleep(1)
        if(gamerID[rID][i].startswith('virtual')):  # if it is a virtual player, just randonly select bet or not
            
            lastPlayer = i
            gamerReply[rID][i] = 1
            if(betStart[rID] == 0):
                betStart[rID] = 1;
                amount = random.randint(1,gamerChip[rID][i]/2)
                chipAmount[rID] = chipAmount[rID]+amount
                gamerChip[rID][i] = gamerChip[rID][i]-amount
                currentChip[rID] = amount                   
            else:
                if(currentChip[rID] > gamerChip[rID][i]):
                    chipAmount[rID] = chipAmount[rID]+gamerChip[rID][i]
                    gamerChip[rID][i] = 0
                else:
                    chipAmount[rID] = chipAmount[rID]+currentChip[rID]
                    gamerChip[rID][i] = gamerChip[rID][i]-currentChip[rID]
            continue
                    
        
        if(betStart[rID] == 0):# betStart[rID] == 0 means this player is the first one to bet, he or she can decide how much to bet
            ID = gamerID[rID][i]
            ip = gamerIP[rID][i]
            numPlayers = numPlayers+1
            mess = 'first '+str(rID)+' '+''+str(','.join(cardInhand[rID][i]))+" "+str(gamerChip[rID][i])+' '+ID      
            send(ip,port,mess)
        else:                 # this player is not the first one to bet, he or she should follow previous players
            ID = gamerID[rID][i]
            ip = gamerIP[rID][i]
            numPlayers = numPlayers+1
            lastPlayer = i
            mess = 'the-bet-amount-is '+str(rID)+' '+''+str(','.join(cardInhand[rID][i]))+" "+str(gamerChip[rID][i])+' '+str(currentChip[rID])+' '+ID            
            send(ip,port,mess)
            for i in range(len(gamerName[rID])):
                if(gamerLeft[rID][i] == 0):
                    numPlayers = numPlayers+1
                    lastPlayer = i
    return numPlayers,lastPlayer

'''def print_pokerstable_state_to_user(mess):
    if mess[0] == 'the-bet-amount-is '
[ , , , , , , ]
[]'''
            
        
def gameStart(rID,gamerID, gamerChip , gameOwner, gamerIP, gamerName, fiveCards, cardInhand,cardLeft):
    while True:
        betStart[rID] = 0     # betStart[rID] should be 0 for each turn of bet
        chipAmount[rID] = 0  # initial the chipAmount[rID] to 0 for each round of game
        currentChip[rID] = 0   # the amount of chips should be bet by the players who is not the first one
        cardLeft[rID] = cards[0:len(cards)] # initial the card deck
        c = gamerChip[rID].count(0)
        if(c == len(gamerChip[rID])-1):# if there is only one player has chip more than 0, the game is over
            s = 'over'
            start[rID] = 0
            broadcast(rID,gamerID,gamerIP,s)
            break
            
        random.shuffle(cardLeft[rID]) # shuffle the card deck
        cardstr = ''
        for i in range(0,len(gamerName[rID])):
            if(len(gamerLeft[rID])<(i+1)):
                gamerLeft[rID].append(0)
            else:
                gamerLeft[rID][i] = 0
            if(len(gamerReply[rID])<(i+1)):
                gamerReply[rID].append(0)
            else:
                gamerReply[rID][i] = 0
            if(len(cardInhand[rID])<(i+1)):
                cardInhand[rID].append([])
            else:
                cardInhand[rID][i].clear()
            cardInhand[rID][i].append(cardLeft[rID].pop())
            cardInhand[rID][i].append(cardLeft[rID].pop())  # each player draws two cards from the deck
        #
        finish = 0
        numPlayers,lastPlayer = bet(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft)
        if(numPlayers <= 1): # if there is only one player bet, game is over and we have the winner
            print('numPlayers ',numPlayers)
            s = "Game end, winner is "+gamerName[rID][lastPlayer]
            broadcast(rID,gamerID,gamerIP,s)
            gamerChip[rID][lastPlayer] = gamerChip[rID][lastPlayer]+chipAmount[rID]
            continue
        
        for i in range(0,3):
            card = cardLeft[rID].pop()
            fiveCards[rID].append(card)
            cardstr = cardstr+card+','
        s = "3 cards are: "+cardstr
        broadcast(rID,gamerID,gamerIP,s) # broadcast the three public cards     
        betStart[rID] = 0 # initial betStart[rID] to 0 for the next turn of bet
        for i in range(0,len(gamerName[rID])):# initial the gamerReply for the next turn of bet 
            if(len(gamerReply[rID])<(i+1)):
                gamerReply[rID].append(0)
            else:
                gamerReply[rID][i] = 0
        numPlayers,lastPlayer = bet(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft)
        if(numPlayers <= 1): # if there is only one player bet, game is over and we have the winner
            print('numPlayers ',numPlayers)
            s = "Game end, winner is "+gamerName[rID][lastPlayer]
            broadcast(rID,gamerID,gamerIP,s)
            gamerChip[rID][lastPlayer] = gamerChip[rID][lastPlayer]+chipAmount[rID]
            continue
        k = 0
        
        while(k<2):# This part of code is to bet for the three more cards
            k = k+1
            betStart[rID] = 0 # initial betStart[rID] to 0 for the next turn of bet
            for i in range(0,len(gamerName[rID])):# initial the gamerReply for the next turn of bet 
                if(len(gamerReply[rID])<(i+1)):
                    gamerReply[rID].append(0)
                else:
                    gamerReply[rID][i] = 0
            card = cardLeft[rID].pop()
            fiveCards[rID].append(card)
            cardstr = cardstr+card+','
            s = str(3+k)+" cards are: "+cardstr
            broadcast(rID,gamerID,gamerIP,s)
            numPlayers,lastPlayer = bet(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft)# start the bet
            if(numPlayers <= 1): # if there is only one player bet, game is over and we have the winner
                print('numPlayers ',numPlayers)
                s = "Game end, winner is "+gamerName[rID][lastPlayer]
                broadcast(rID,gamerID,gamerIP,s)
                gamerChip[rID][lastPlayer] = gamerChip[rID][lastPlayer]+chipAmount[rID]
                finish = 1
                break
        if(finish): # if finish means there is only one player bet, game is over and we have the winner, so go to the next game
            continue
        updateInfo(rID,gamerID, gamerChip, gamerIP, gamerName, cardInhand,cardLeft) # broadcast the information to all clients
        s = "Game end, winner is "+gamerName[rID][0] # if there are more than one person still in the game after drawing all five cards, just choose the first one win. Because I haven't implemneted the winning rule yet
        broadcast(rID,gamerID,gamerIP,s)
        gamerChip[rID][lastPlayer] = gamerChip[rID][lastPlayer]+chipAmount[rID]
    
def handle(incoming_buffer, roomID, gamerID, gamerChip , gameOwner, gamerIP, gamerName, cardLeft):# cope with the message listened
    while True:
        time.sleep(0.05)
        # okay so each client is interacting with the same port/address/socket
        if len(incoming_buffer)>0:            
            s = incoming_buffer.pop()
            if(s.startswith("create")):              # means someone want to create a room for game
                name,ID,chip,ip = getcreate(s)
                if(roomID == 100):
                    mess = "100 rooms already"+" "+ID
                    send(ip,port,mess)
                    continue
                gamerName[roomID].append(name) # add the players name ,ID,Ip and chip to this room.
                gamerID[roomID].append(ID)
                gamerIP[roomID].append(ip)
                gamerChip[roomID].append(int(chip))
                gameOwner[roomID] = name      # set the owner of this room to this player because he or she creates the room
                mess = "create "+str(roomID)+" "+ID
                send(ip,port,mess)
                roomID = roomID+1           
            if(s.startswith("start")): #whether start game or not in this room
                name,ID,chip, rID, ip = getjoin(s)
                if(gameOwner[rID] == name and start[rID] == 0):# only the owner of the room can start the game
                    if(len(gamerID[rID]) >= 2): # if there are more than one plyer in the room, start it
                        s = 'start '
                        broadcast(rID,gamerID,gamerIP,s)
                        start[rID] = 1
                        cardLeft[rID] = cards[0:len(cards)]
                        t = threading.Thread(target=gameStart,args=(rID,gamerID, gamerChip , gameOwner, gamerIP, gamerName, fiveCards, cardInHand,cardLeft))
                        t.start()
                        
                    elif(len(gamerID[rID]) == 1):# if there is only one player,add a stupid virtual player
                        s = 'start '
                        broadcast(rID,gamerID,gamerIP,s)
                        name = 'virtualplayer'
                        ID = 'virtual ID'
                        chip = 100
                        ip = 'virtual IP'
                        gamerName[rID].append(name)
                        gamerID[rID].append(ID)
                        gamerIP[rID].append(ip)
                        gamerChip[rID].append(int(chip))
                        s = 'start '
                        broadcast(rID,gamerID,gamerIP,s)
                        start[rID] = 1
                        t = threading.Thread(target=gameStart,args=(rID,gamerID, gamerChip , gameOwner, gamerIP, gamerName, fiveCards, cardInHand,cardLeft))
                        t.start()
            if(s.startswith("join")): # there is one player want to join the existing game 
                name,ID,chip, rID, ip = getjoin(s)
                if(gameOwner[rID] != ''):
                    if(ID in gamerID[rID] and ip in gamerIP[rID]): # check whether the ID and IP are the same, you cannot have the same ID and IP in one room
                        mess = "sameID"+" "+ID
                        send(ip,port,mess)
                        continue
                    if(len(gamerID[rID]) == 10):# if there are 10 people in the room, you are rejected
                        mess = "ten people already"+" "+ID
                        send(ip,port,mess)
                        continue
                    if(start[rID] == 1): # if the game has started, you are rejected
                        mess = "Already start"+" "+ID
                        send(ip,port,mess)
                        continue
                    gamerName[rID].append(name)
                    gamerIP[rID].append(ip)
                    gamerChip[rID].append(int(chip))
                    mess = "join successfully "+str(roomID)+" "+ID
                    send(ip,port,mess)
            if(s.startswith("bet-start")): # this message means that there is a player want to bet and he is the first one to bet
                info = s.split(' ')
                rID = int(info[2])
                index = gamerName[rID].index(info[3])
                amount = int(info[1])
                gamerChip[rID][index] = gamerChip[rID][index]-amount
                if(currentChip[rID] == 0):
                    currentChip[rID] = amount # set the currentChip[rID] to the amount of chips this player bet, because he is the first one 
                gamerReply[rID][index] = 1 # set gamerReplay[rID][index] to 1 means that the next player can bet, because this player has already replied 
                chipAmount[rID] = chipAmount[rID]+amount# add the amount of chip he or she bets to the chipAmoun[rID]
                betStart[rID] = 1
                s = "Player "+info[3]+" bet"
                print("recieved bet from "+info[3])
                broadcast(rID, gamerID,gamerIP,s) # broadcast whether he bet or not to all players
            if(s.startswith('n')): # means this player decide not to bet
                info = s.split(' ')
                rID = int(info[1])
                index = gamerName[rID].index(info[2])
                gamerReply[rID][index] = 1# set gamerReplay[rID][index] to 1 means that the next player can bet, because this player has already replied 
                gamerLeft[rID][index] = 1# set gamerLeft[rID][index] to 1 means this player will not bet in the next turn of bet in this round of game 
                s = "Player "+info[2]+" doesn't bet"
                broadcast(rID, gamerID,gamerIP,s)# broadcast whether he bet or not to all players
                
def listen(ip, port, incoming_buffer):
    #print("Server is starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '192.168.2.3'
    sock.bind((ip, port))
    sock.listen(5)
    #print("Server is listenting port 8001, with max connection 5")
    while True:
        connection, address = sock.accept()
        try:
            connection.settimeout(10000)
            buf = connection.recv(1024)
            s = buf.decode("utf-8")
            sfull = s+" "+address[0]
            # incoming_buffer on the server side is a globally shared list of tcp connections
            incoming_buffer.append(sfull)
            print("sfull is "+sfull)
        except socket.timeout:
            print('time out')

ip = 'localhost'
port = 8001
incoming_buffer = []
t1 = threading.Thread(target=listen,args=(ip, port, incoming_buffer))
t1.start()
t2 = threading.Thread(target=handle,args=(incoming_buffer, roomID, gamerID, gamerChip , gameOwner, gamerIP, gamerName, cardLeft))
t2.start()