import random, time
#check if Python 3 or 2.7
from sys import version_info
py3 = version_info[0] > 2 

def my_input(text):

	if py3:
		return input(text)
	else:
		return raw_input(text)	

#message returned after every turn
def in_game_status(still_in_game):
    if still_in_game:
        message="\nPlayer value is " + str(my_hand.get_value())
        message+= ", and contains "+my_hand.__str__()
        message+="\nDealer Hand contains "+dealer_hand.list_of_cards[0].__str__()
        message+=" (one card hidden)"
        message+="\nDealer value is "+str(dealer_hand.get_value())
        message+= "\nDealer Hand contains "+dealer_hand.__str__()
    else:
        message="\nPlayer value was " + str(my_hand.get_value())
        message+= ", and contained "+my_hand.__str__()
        message+="\nPlayer has $"+str(total_cash)+" left."
        message+="\nDealer value was "+str(dealer_hand.get_value())
        message+= "\nDealer Hand contained "+dealer_hand.__str__()
    return message

#define event handlers for deal, hit, stand, and split
def deal():
    global total_cash, in_play, deck, my_hand, dealer_hand

    in_play = True
    # your code goes here
    deck = Deck()
    deck.shuffle()
    
    my_hand = Hand()
    dealer_hand = Hand()
    for i in range(2):
        #Deal card to my hand then dealer's, two times.
        my_hand.add_card( deck.deal_card() )
        dealer_hand.add_card( deck.deal_card() )
    return in_game_status(True)

def hit():
    global total_cash, in_play, deck, my_hand, dealer_hand
    
    if not in_play: 
        return "'not in play' error in the hit function."
    my_hand.add_card( deck.deal_card() )
    if my_hand.get_value() <= 21:
        message = in_game_status(True)
    elif my_hand.get_value() > 21:
        message = "YOU LOSE! You have busted!"
        message += in_game_status(False)
        total_cash -= my_bet
        in_play = False
    return message
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and total_cash

def stand():
    global total_cash, in_play, deck, my_hand, dealer_hand
    
    message = ""
    if not in_play: #never applicable
        return "hmmm"
    if my_hand.get_value() > 21:
        message = "YOU LOSE! You have busted!"
        message += in_game_status(False)
        total_cash -= my_bet
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card( deck.deal_card() )
            
        if dealer_hand.get_value() > 21:
            message = "Dealer busted! YOU WON!!!"
            message += in_game_status(False)
            total_cash += my_bet
        else:
            if my_hand.get_value() > dealer_hand.get_value():
                message = "\nYOU WON!!!"
                message += in_game_status(False)
                total_cash += my_bet
            elif my_hand.get_value() == dealer_hand.get_value():
                message = "\nYOU PUSH"
            else:
                message = "\nYOU LOSE."
                message+= in_game_status(False)
                total_cash -= my_bet
    in_play = False
    return message
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    def __str__(self):
        return self.rank+" of "+self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
       
# define hand class
class Hand:
    def __init__(self):
        self.list_of_cards = []	# create Hand object

    def __str__(self):
        str = ""
        for card in self.list_of_cards:
            str += card.__str__() +", "
        str = str[:-2] #remove comma at end
        return str    
    def add_card(self, card):
        self.list_of_cards.append(card)
        
    def get_value(self):
        hand_value = 0
        has_ace = False
        for card in self.list_of_cards:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'Ace':
                has_ace = True
        if not has_ace:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
     
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                card = Card(suit, rank)
                self.deck.append(card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        last_index = len(self.deck) - 1
        card_to_deal = self.deck[last_index]
        self.deck.pop(last_index)
        return card_to_deal
        # deal a card object from the top of the deck, and remove it
        
    def __str__(self):
        str = ""
        for card in self.deck:
            str += " " + card.__str__()
        return "Deck contains" + str

# define globals for cards
SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
RANKS = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
VALUES = {'Ace':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10}

# initialize some useful global variables
in_play = False
program_running = True
instructions = ""
total_cash = 50
my_bet = 0
#deck = Deck()

def initialize_bet():
    has_given_int = False
    print("You have $"+str(total_cash)+". How much would you like to bet?")
    
    while not has_given_int:
        bet_response = my_input("Please enter an integer from 1 to "+str(total_cash)+" inclusive.\n")

        if type(bet_response)==int:
            bet_response_int = int(bet_response)
            if 1<=bet_response_int and bet_response_int<=total_cash:
                has_given_int = True
    print("You have $"+str(total_cash)+" and your bet is $"+str(bet_response)+".")
    return bet_response


welcomeMessage="Welcome to Blackjack by Pranay Mittal!\nHit enter to start a new game!"
my_input(welcomeMessage)
while program_running:
    my_bet = int(initialize_bet())
    time.sleep(2) #wait 2 seconds?
    response = my_input(deal()+"\nType h for hit, s for stand, or g for split.\n")
    while in_play:
        if response == 'h':
            response_message = hit()
            if in_play:
                response_message += "\nType h for hit, s for stand, or g for split.\n"
                response = my_input(response_message)
            else:
                print(response_message)
        elif response == 's':
            response = stand()
            print(response)
        #NEED TO IMPLEMENT SPLIT
        else:
            response = my_input("Type h for hit, s for stand, or g for split.\n")
    if(total_cash <= 0):
        print("You are out of money. Game over.")
        break
    again_input = "Game is over.\nType yes to play again. "
    again_input += "Type anything else to end the program.\n"
    again_response = my_input(again_input)
    if again_response != "yes":
        program_running = False
print("Program is terminated.")


