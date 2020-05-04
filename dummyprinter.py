import numpy as np
import random

class CardDeck:
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
    

class Player:
    def __init__(self, pid, personal_hand, starting_balance, is_creator, ip_address):
        self.pid = pid
        self.is_creator = is_creator
        self.personal_hand = personal_hand
        self.starting_balance = starting_balance
        self.current_balance_server = starting_balance
        self.myturn = False
        self.winner = False
        self.status = "Active" # might otherwise be folded
        self.ip_address = ip_address
        
    def __str__(self):
        return str(self.pid)+"("+self.status+", has $"+str(self.current_balance_server)+")"
    
class PokerTable:
    def __init__(self, first_player,game_id):
        self.game_id = game_id
        self.deck = CardDeck()
        self.bet_round = 1
        self.game_started = False # aka bet_round is zero
        self.pot = 0
        self.call_amount = 0
        self.public_cards = ['~','~','~','~','~']
        self.player_list = [first_player]
        self.betting_round_player_bets = [0]
        self.curr_player_idx = 0
        self.first_player = first_player
        
        
    def add_player(self, new_player, game_id):
        if not self.game_started:
            self.player_list.append(new_player)
            self.betting_round_player_bets.append(0)
        
    def whos_turn(self):
        return self.curr_player_idx
    
    def update_call_amount(self):
        call = 0
        for amount in self.betting_round_player_bets:
            if amount > call:
                call = amount
        self.call_amount = call
        
#     def print_status(self):
#         print("------------------------------\n")
#         print("Betting round: " + str(self.bet_round))
#         print("Current pot: $"+str(self.pot))
#         print("Public hand: "+str(self.public_cards))
#         print("Players (in betting order): ")
#         print([player.pid for player in self.player_list])
#         print("Player accounts:")
#         print([player.current_balance_server for player in self.player_list])
#         print(self.player_list.__getitem__(self.curr_player_idx%len(self.player_list)))     
        
    def __str__(self):
        tidx = (self.curr_player_idx%len(self.betting_round_player_bets))
        return "------------------------------------------------------------------"+\
            "\nGame id: "+str(self.game_id)+", Pot size: $"+str(self.pot)+", Betting round: "+str(self.bet_round)+ \
            "\nPlayers (betting order):"+\
            "\n"+" // ".join(str(x) for x in self.player_list)+\
            "\nCards: ["+", ".join(str(x) for x in self.public_cards)+"]"+\
            "\nPot: $"+str(self.pot)+\
            "\nRound bets: ["+', '.join(str(x) for x in self.betting_round_player_bets)+"]"+\
            "\n"+str(self.player_list[tidx])+'\'s turn to bet...($'+\
            str(self.call_amount - self.betting_round_player_bets[tidx])+' to call)'
            # str(self.call_amount - self.betting_round_player_bets[self.curr_player_idx%len(self.betting_round_player_bets)])+' to call)'
            
# class SetupInfo:
#     def__init__(self, join, start, setupPhase):
#         self.setupPhase = setupPhase    # this is 1, 2, or 3
#         if(join ^ start):
#             self.join = join
#             self.start = start
#         else:
#             return
#         self.joinSuccess = 
        
#setup  # I am a player and want to create a new table
#setup  # I am a player and want to join an existing table (tableID X)
#setup  # I am the player1 and want to start the game with this table now
#setup  # I am a player and I give you control to my money (amount, password)
#setup  # I am the server and you have created a new table (tableID X)
#setup  # I am the server and you have joined an existing table (gameID X)
#setup  # I am the server and you have failed to join the table (gameID X)
#setup  # I am the server and a new player has joined the table (player X)
#setup  # I am the server and players at the table are: [a, b, c, d]
#setup  # I am the server and I return you control of your money
#setup  # I am the server and we are starting the game
#setup  # I am the server and something went wrong try again
        
#         sc = "server" # or "client"
#         cj = "create" # or "join" or "X"
#         starter = 1 # or 0 (sent by server)
#         sendmoney = 1 # or 0
#         moneyamount = 4334141 # also sendmoney must be 1 otherwise it's 0
#         ackmoneyreceived = 1 # or 0
#         newtablesuccess = 1 # or 0 also starter must be 0 or 1
#         jointablesuccess = 1 # or 0 also starter should be -1
#         newplayerjoined = 1 # or 0
#         newplayername = "string"
#         playerlist = [list of strings]
#         gameStarted = 1 or 0
#         errortryagain = 1 or 0
        

#game   # I am the server and this is the table update
#game   # I am a player and it's my turn and this is my bet
        sc = "server" # or "client"
        table = tableinfo
        bet = betamount
    
# def serialize_private_cards(cardlist):
#     return "privatecards$"+",".join(cardlist)

# def deserialize_private_cards(pcstring):
#     return pcstring.split("$")[1].split(",")

# def serialize_setup_message():

# def deserialize_setup_message():
    

#def serialize_


p1 = Player('Mickey',['X','X'],10000.83,True,"")
p2 = Player('Goofy',['X','X'],8000.3,False,"")
p3 = Player('Kramer',['X','X'],55600.00,False,"")
p4 = Player('Pinocchio',['X','X'],10000,False,"")


bet11 = 50
bet21 = 60
bet31 = 100
bet41 = 100
bet12 = 50 
bet22 = 0 # 0 to fold
bet32 = 'na'
bet42 = 'na'

pt = PokerTable(p1,1)
pt.add_player(p2,1)
pt.add_player(p3,1)
pt.add_player(p4,1)
print("Game Start!")
print(pt)
################################################
# Mickey bets 50
pt.pot+= bet11
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet11
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet11
pt.update_call_amount()
pt.curr_player_idx+= 1
print(pt)
# Goofy bets 60
pt.pot+= bet21
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet21
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet21
pt.update_call_amount()
pt.curr_player_idx+= 1
print(pt)
# Kramer bets 100
pt.pot+= bet31
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet31
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet31
pt.update_call_amount()
pt.curr_player_idx+= 1
print(pt)
# Pinocchio
pt.pot+= bet41
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet41
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet41
pt.update_call_amount()
pt.curr_player_idx+= 1
print(pt)
# Mickey sees 50
pt.pot+= bet12
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet12
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet12
pt.update_call_amount()
pt.curr_player_idx+= 1
print(pt)
# Goofy folds
pt.pot+= bet12
pt.player_list[pt.curr_player_idx%len(pt.player_list)].current_balance_server-= bet12
pt.betting_round_player_bets[pt.curr_player_idx%len(pt.player_list)]+=bet12
pt.update_call_amount()
pt.player_list[pt.curr_player_idx%len(pt.player_list)].active = "Folded"
pt.curr_player_idx+= 1
# If for all "Active" players, they have an equal amount bet, then we announce
print("Betting round "+str(pt.bet_round)+" over!")
pt.betting_round_player_bets = [0 for x in pt.betting_round_player_bets]
pt.bet_round += 1
pt.call_amount = 0
pt.curr_player_idx = 0
pt.public_cards[0] = "A Spd"
pt.public_cards[1] = "K Jck"
pt.public_cards[2] = "2 Dmd"
print(pt)

x = 0
while True:
    x +=1
