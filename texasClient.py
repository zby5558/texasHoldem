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
ml = []
roomID = '1'
ID = random.randint(1,10000) #since we do not have enough machine, each machine can be used as several clients. Thus ID is used to distingush different players in one machine(haven't be implemented yet)
def handle(ml, ipServer): # not used
    while True:
        # ml definition: list for saving incoming messages      
        if len(ml)>0:            
            s = ml.pop()
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
            
                
            
def listen(ip, port, ml): # listen the feedback from the server
    #print("Server is starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ip: is the local ip address
    ip = '192.168.2.4'
    print(ip)
    sock.bind((ip, port))
    sock.listen(5)
    #print("Server is listenting port 8001, with max connection 5")
    while True:
        time.sleep(0.05)
        connection, address = sock.accept()
        try:
            connection.settimeout(10000)
            buf = connection.recv(1024)
            s = buf.decode("utf-8")
            sfull = s+" "+address[0]
            ml.append(sfull)
            print(s)
        except socket.timeout:
            print('time out')
def send(ip,port,mess):  #send function is used to send message to the taxasSever
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((ip, port))
    byt = mess.encode()
    sock.send(byt)
def createGame(ip,port,name,ID, chip):
    mess = "create "+name+" "+str(ID)+" "+str(chip)
    send(ip, port, mess)
def joinGame(ip,port,name,ID, chip, roomID):
    mess = "join "+name+" "+str(ID)+" "+chip+" "+str(roomID)
    send(ip, port, mess)
def startGame(ip,port,name,ID, chip, roomID):
    mess = "start "+name+" "+str(ID)+" "+chip+" "+str(roomID)
    send(ip, port, mess)
#name = input("Enter your name : ") #input yout own name
name = 'boyang'
port = 8001
print("Your name is "+name)
      
#chip = input("Enter your chip : ") # input your chip which is used to bet
chip = '100'
print("your chip is "+chip)
#ipServer = input("ip address of the texasSever : ") # ipAddress of the server, the client can only send message to the server and receive the message from the server
ipServer = '192.168.2.5'
print("your ip sever is "+ipServer)
ip = '127.0.0.1'
t1 = threading.Thread(target=listen,args=(ip, port, ml))#create one thread keep listening from the server, all the information receiverd is added to list ml
t1.start()

cg = input("do you want you create game? please use y or n : ") #whether you want to create a room for game or not
if cg == 'y':
    createGame(ipServer,port, name,ID,chip) #send create request to the server
    while True:   
        if len(ml)>0:            
            s = ml.pop()
            info = s.split(' ')
            selfID = info[len(info)-2]
            ip = info[len(info)-1]
            if(ip == ipServer and int(selfID) == ID): # since each machine can be server clients with different id, so the client only deal with feedback from the server with its own id
                if(s.startswith("create")):                   
                    roomID = info[1]
                    print("create successfully and the room ID is "+roomID)#create successfully and get the roomID, this client is the owner of the game
                    break
    print("room id : "+roomID)
    sg = input("do you want to start the game? use y or n : ")
    if sg == "y":
        startGame(ipServer,port,name,ID,chip, roomID) #send start request to the server
        while True:  
            time.sleep(0.05)
            if len(ml)>0:            
                s = ml.pop()
                info = s.split(' ')
                selfID = info[len(info)-2]
                ip = info[len(info)-1]
                if(ip == ipServer and int(selfID) == ID):
                    if(s.startswith("start")):                   #if received start, means we sucessfully start the game
                        print("start successfully and the room ID is "+roomID)
                        while True:
                            time.sleep(0.05)
                            if len(ml) == 0:
                                continue
                            s = ml.pop()
                            info = s.split(' ')
                            selfID = info[len(info)-2]
                            ip = info[len(info)-1]
                            if(ip == ipServer and int(selfID) == ID):#check whether the sender is the Server and send to our ID
                                if(s.startswith('over')):
                                    print('gameOver')
                                    sys.exit()
                                if(s.startswith('name') or s.startswith('chip') or s.startswith('card')):
                                    print(info[0])
                                if(s.startswith('You-are')):
                                    
                                    print("your card in hand: " + info[len(info)-4])
                                    bet = input("do you want to start the bet? y or n: ") # means you are the fisrt one to bet
                                    if(bet == 'y'):
                                        amount = input("how much do you want to bet?")# how many chips do you want to bet
                                        print("you have "+info[len(info)-3]+" chip")
                                        print("your card in hand is "+info[len(info)-4])
                                        while(int(amount)>int(info[len(info)-3]) or int(amount) == 0):# you bet amount should be less than the chips you have
                                            amount = input("you do not have enough money or you input no money, reinput it: ")
                                        mess = "bet-start "+amount+" "+roomID+" "+name
                                        send(ipServer,port, mess)
                                    else:
                                        mess = 'n '+roomID+" "+name
                                        send(ipServer,port, mess)
                                if(s.startswith('the-bet')):#Previously, there is someone bet, do you want to follow him
                                    print("do you want to follow the bet? the bet amount is "+info[len(info)-3])
                                    print("you have "+info[len(info)-4]+" chip")
                                    print("your card in hand is "+info[len(info)-5 ])
                                    bet = input(" y or n: ")
                                    if(bet == 'y'):
                                        if(info[len(info)-3] > info[len(info)-4]):# if you do not have enough chips, and you choose yes, just show hand 
                                            amount = int(info[len(info)-4])
                                        else:
                                            amount = int(info[len(info)-3])
                                        mess = "bet-start "+amount+" "+roomID+" "+name
                                        send(ipServer,port, mess)
                                if(s.startswith('Game end') or s.startswith("Player") or s.startswith("three")):#this is to check whether this round of game is end, or does the player bet or not ,or who is the winner of the game
                                    '''info = s.split(' ')
                                    info = info[0:len(info)-2]
                                    print(" ".join(info))'''
                                    print(s)
                                    
                    elif(s.startswith("fail")):
                        print("fail to start")
                        sys.exit()
                        
    
else:
    jg = input("do you want you join game? please use y or n : ") # whether to join a game whose owner is anothet client
    if jg == 'y':
        roomID = input("roomID is : ")                  #if you want to join the name, you need to know the roomID from the gameOwner
        joinGame(ipServer,port,name,ID, chip, roomID)  
        while True:   
            if len(ml)>0:            
                s = ml.pop()
                info = s.split(' ')
                selfID = info[len(info)-2]
                ip = info[len(info)-1]
                if(ip == ipServer and int(selfID) == ID):
                    if(s.startswith("join")):                   
                        roomID = info[1]
                        print("join successfully and the room ID is "+roomID)
#t3 = threading.Thread(target=start,)
#t3.start()

