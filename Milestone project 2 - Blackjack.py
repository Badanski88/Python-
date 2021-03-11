#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9,'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11, 'Ace':1}

playing = True


# In[2]:


class Card():
    
    def __init__(self, suit, rank):
    
        self.suit = suit
        
        self.rank = rank
        
        self.value = values[rank]
        
    def __str__(self):
        
        return self.rank + " of " + self.suit
    


# In[3]:


one_card = Card('Hearts', 'Ten')


# In[4]:


print(one_card)


# In[5]:


class Deck():
    
    def __init__(self):
        
        self.deck = []           #start with an empty list
        
        for suit in suits:
            
            for rank in ranks:   #Create the Card Object
                
                created_card = Card(suit, rank)
                
                self.deck.append(created_card)
                
    def shuffle(self):
        
        random.shuffle(self.deck)
        
    def deal(self):
        
        return self.deck.pop()
        
    def __str__(self):
        
        return f'Currently there are {len(self.deck)} cards left in the deck'


# In[6]:


test_deck = Deck()
print(test_deck)


# In[7]:


class Hand():
    
    def __init__(self):
        
        self.cards = []   # start with an empty list as we did in the Deck class
        self.value = 0    # start with zero value
        self.aces = 0     # add an attribute to keep track of aces
        
    def add_card(self,card):
        
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank =='Ace':
            self.aces +=1 #add to self.aces
            
        
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -=1
       
            


# In[8]:


test_deck = Deck()
test_deck.shuffle()
test_player = Hand()
test_player.add_card(test_deck.deal())
test_player.add_card(test_deck.deal())
test_player.value


# In[9]:


class Chips():
    def __init__(self):
        self.total = 100 # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total +=self.bet
            
    def lose_bet(self):
        self.total -=self.bet        


# In[10]:


#Step 6 function for taking bets

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer')
        else:
            if chips.bet > chips.total:
                print('Sorry not enough chips in your account, you have', chips.total)
            else:
                break
        


# In[11]:


#Step 7: function for taking hits

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


# In[12]:


#function prompting the Player to Hit or Stand

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        x = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if x[0].lower() == 'h':
            hit(deck,hand)  # hit() function defined above

        elif x[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


# In[13]:


# Step 9:  functions to display cards

def show_some(player, dealer):
    print("\n Dealer's hand:")
    print("<card hidden>")
    print('', dealer.cards[1])
    print("\n Player's hand:", *player.cards, sep='\n ')

    
def show_all(player, dealer):
    print("\nDealer's hand:", *dealer.cards, sep='\n ')
    print("Dealer's hand =", dealer.value)
    print("\nPlayer's hand:", *player.cards, sep='\n ')
    print("\n Player's hand =", player.value)


# In[14]:


#Step 10: Write functions to handle end of game scenarios


# In[15]:


def player_busts(player, dealer, chips):
    print('Player busts')
    chips.lose_bet()


# In[16]:


def player_wins(player, dealer, chips):
    print('Player wins!')
    chips.win_bet()


# In[17]:


def dealer_busts(player, dealer, chips):
    print('Dealer busts!')
    chips.win_bet()


# In[18]:


def dealer_wins(player, dealer, chips):
    print('Dealer wins!')
    chips.lose_bet()


# In[19]:


def push(player, dealer):
    print('Dealer and Player tie! Its a push.')


# # And now on to the game!!

# In[ ]:


while True:
    # Print an opening statement
    
    print('Hello, welcome to Blackjack! Get as close to 21 as you can without going over!\n    Dealer hits until he reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player

    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    
    player_chips = Chips()
    
    # Prompt the Player for their bet
    
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)

    show_some(player_hand, dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        
        
        # Prompt for Player to Hit or Stand
        
        hit_or_stand(deck, player_hand)
        
        # Show cards (but keep one dealer card hidden)
 
        show_some(player_hand, dealer_hand)
    
        # If player's hand exceeds 21, run player_busts() and break out of loop
        
        if player_hand.value > 21:

            player_busts(player_hand, dealer_hand, player_chips)

            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    
    if player_hand.value <= 21:
            
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
    
        # Show all cards
        
        show_all(player_hand, dealer_hand)
    
        # Run different winning scenarios
        
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
            
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
            
        else: 
            push(player_hand, dealer_hand)
        
    # Inform Player of their chips total 
    
    print('Currently you have' , player_chips.total)
    
    # Ask to play again
    new_game = input("Would you like to play again? Please type 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True 
        continue
    else:
        print('Thank you for playing')
        break


# In[ ]:





# In[ ]:




