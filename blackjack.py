#! python3

# name          :       BlackJack
# Programmer    :       Damian Duffy | https://github.com/damianduffy/
# Version       :       1.0
# Release Date  :       6th April 2018
# Description   :       Blackjack game.  Opjective is to get 21 or closer to 21
#                       than the computer dealer without going over 21.  Each
#                       round bets 100 points and you start with 1,000 points.
#                       Win a round and you get 150 points.  Lose and you're
#                       down 100 points.


# import required modules
import sys                  # required for fonts & exit
import os                   # required to load images
import random               # reqired to shuffle deck
import pygame               # required for graphics, etc.
from pygame.locals import * # required for graphics, etc.

# global variables
bet = 100                   # default bet amount
state = 0                   # used to control the game state

# Initialize game engine and clock
pygame.init()
clock = pygame.time.Clock()

# setup the display canvas
SCREENSIZE = [800, 400]
screen = pygame.display.set_mode(SCREENSIZE)
pygame.mouse.set_visible(False)
pygame.display.set_caption("BlackJack")

# setup fonts for text
pygame.font.init()
large_font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 15)
text_colour = (255, 255, 0)

# Text message content
MSG_EXIT = "Are you sure you want to quit? [y/n]"
MSG_PAUSE = "Game paused.  Press [p] to resume."
MSG_HIT_OR_STAND = "Press [h] to hit or [s] to stand"
MSG_DEAL = "Press [n] to start a new game."
MSG_DRAW = "Draw hand.  Press [d] to deal again."
MSG_PLAYER_WINS = "Player wins.  Press [d] to deal again."
MSG_DEALER_WINS = "Dealer wins.  Press [d] to deal again."
MSG_PLAYER_BUST = "Dealer wins - player bust.  Press [d] to deal again."
MSG_DEALER_BUST = "Player wins - dealer bust.  Press [d] to deal again."
msg_game = small_font.render("Press [h] to hit or [s] to stand", False, (0, 0, 0))


# Load images
def load_image(name, colorkey = None):
    fullname = os.path.join('cards/', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        print(os.getcwd())
        raise SystemExit(message)

    if colorkey is not None:
        image = image.convert()
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    else:
        image = image.convert_alpha()

    return image


# add images to appropriate cards in the deck
def load_images_to_pack(pack):
    cards = list(pack.keys())
    for card in cards:
        pack[card].append(load_image(card + ".png"))
    return pack


class CardDeck:
    def __init__ (self):
        self.pack = {
            "SA": [1], "S2": [2], "S3": [3], "S4": [4], "S5": [5], "S6": [6], "S7": [7], "S8": [8], "S9": [9], "S10": [10], "SJ": [10], "SQ": [10], "SK": [10],
            "CA": [1], "C2": [2], "C3": [3], "C4": [4], "C5": [5], "C6": [6], "C7": [7], "C8": [8], "C9": [9], "C10": [10], "CJ": [10], "CQ": [10], "CK": [10],
            "HA": [1], "H2": [2], "H3": [3], "H4": [4], "H5": [5], "H6": [6], "H7": [7], "H8": [8], "H9": [9], "H10": [10], "HJ": [10], "HQ": [10], "HK": [10],
            "DA": [1], "D2": [2], "D3": [3], "D4": [4], "D5": [5], "D6": [6], "D7": [7], "D8": [8], "D9": [9], "D10": [10], "DJ": [10], "DQ": [10], "DK": [10]
        }
        self.deck = []
        self.back_image = load_image("BackBlue1.png")


    # fill the deck list and randomly shuffle it
    def shuffle(self):
        self.deck = []
        for pack in range(0, 6):
            self.deck += list(self.pack.keys())
        random.shuffle(self.deck)

    # take a card from the deck and return it
    def draw_card(self):
        return self.deck.pop(0)

    # return a list of the cards in the deck
    def get_deck(self):
        return self.deck

    # return the value of the card being queried
    def get_value(self, card):
        return self.pack[card][0]

    def load_card_images(self):
        self.pack = load_images_to_pack(self.pack)

    def get_card_image(self, card):
        return self.pack[card][1]

    def get_num_cards_in_deck(self):
        return len(self.deck)


class Player:
    def __init__ (self):
        self.score = 1000
        self.hand = []
        self.count = 0
        self.has_ace = False
        self.name = "Player"
        self.wager = bet

    # place a bet
    def bet(self, amount = None):
        # allow for optional custom wager amount
        if amount == None:
            amount = bet
        # if insufficient funds, bet maximum
        if amount >= self.score:
            amount = self.score
        # if no money left...
        if amount == 0:
            # not doing anything in this scenario but could offer option for new game
            pass
        # set the wager and decrement from score
        self.wager = amount
        self.score -= self.wager

    # return the current amount bet
    def get_wager(self):
        return self.wager

    # take a card
    def hit(self, deck):
        # add the new card to player's hand
        card = deck.draw_card()
        if card[1] == "A":
            self.has_ace = True
        self.hand.append(card)
        # refresh the count of card values
        count = 0
        for card in self.hand:
            count += deck.get_value(card)
        # check if the player has an Ace and count it as 11 (once it doesn't bust)
        if self.has_ace == True and (count + 10) <= 21:
            count += 10

    # don't take a card / hold / stand
    def stand(self):
        global state
        print(self.name, "is standing")
        state += 1

    # reset the score to 0 for new game
    def reset_score(self):
        self.score = 0

    # increment the score
    def scored(self, rate = None):
        if rate == None:
            self.score += (self.wager * 1.5)    # default payout is 1.5 times wager
        else:
            self.score += (self.wager * rate)
        self.wager = 0

    # return the current score
    def get_score(self):
        return self.score

    # return the count based on the current held cards
    def get_count(self, deck):
        count = 0
        for card in self.hand:
            count += deck.get_value(card)
        # check if the player has an Ace and count it as 11 (once it doesn't bust)
        if self.has_ace == True and (count + 10) <= 21:
            count += 10
        return count

    # return a list of the cards held
    def get_hand(self, card = -1):
        if card == -1:
            return self.hand
        else:
            return self.hand[card]

    # clear the cards held by the player
    def reset_hand(self):
        self.hand = []
        self.has_ace = False

    # return how many cards the player has
    def get_num_cards(self):
        return len(self.hand)

    def get_name(self):
        return self.name

    # display the player hand
    def display_cards(self, deck, cover = 5):
        # Display the card graphics
        # determine the position to display the cards
        if self.name == "Player":
            ypos = 180
        else:
            ypos = 20
        xpos = 20

        for card in range(0, self.get_num_cards()):
            # check if the card should be face-down
            if cover < 4 and card == 0:
                # display the face-down card
                screen.blit(deck.back_image, (xpos, ypos))
                cover -= 1
            else:
                # display the card
                screen.blit(deck.get_card_image(self.get_hand(card)), (xpos, ypos))
            xpos += 110

    # update tasks for the player's turn
    def update(self):
        # does nothing.  Method override in Dealer class
        pass


class Dealer(Player):
    def __init__ (self):
        Player.__init__(self)
        self.name = "Dealer"

    def update(self, deck):
        count = self.get_count(deck)
        while count < 17:
            self.hit(deck)
            self.display_cards(deck)
            count = self.get_count(deck)
        else:
            self.stand()


# Deal two cards to each player
def deal(deck, dealer, player):
    # clear both hands of cards
    player.reset_hand()
    dealer.reset_hand()
    # if the shoe is running low on cards; refill with new deck
    if deck.get_num_cards_in_deck() < 78:
        deck.shuffle()
    # deal two cards to each player
    for cards in range(0, 2):
        player.hit(deck)
        dealer.hit(deck)


# End the program
def exit_game():
    exit = 0
    #pygame.mixer.pause()
    exit_msg = large_font.render("Are you sure you want to quit? [y/n]", False, text_colour)
    while exit == 0:
        screen.blit(exit_msg, (200, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.quit()
                    sys.exit()
                if event.key == K_n:
                    exit = -1
                if event.key == K_SPACE:
                    exit = -1
                    new_game()
    #pygame.mixer.unpause()


# Pause the game
def pause_game():
    pause = 0
    #pygame.mixer.pause()
    pause_msg = large_font.render("Press [p] to resume game", False, (0, 0, 0))
    while pause == 0:
        screen.blit(pause_msg, (200, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pause = -1
    #pygame.mixer.unpause()


def key_down(event, player = None, deck = None):
    global state

    if event.key == K_ESCAPE:
        exit_game()
    if event.key == K_h:
        if state == 3:
            player.hit(deck)
    if event.key == K_s:
        if state == 3:
            player.stand()
    if event.key == K_n:
        if state == 0 or state >= 5:
            state = 1
    if event.key == K_d:
        if state >= 5:
            state = 2
    if event.key == K_p:
        pause_game()


def update_display(state, player = None, dealer = None, deck = None):
    global bet, MSG_EXIT, MSG_PAUSE, MSG_HIT_OR_STAND, MSG_DEAL, MSG_DRAW, MSG_PLAYER_WINS, MSG_DEALER_WINS, MSG_PLAYER_BUST, MSG_DEALER_BUST

    # fill the green background
    screen.fill((7,99,36))

    # display on-screen instructions
    msg_instructions1 = small_font.render("Press [p] to pause", False, (0, 0, 0))
    msg_instructions2 = small_font.render("Press [esc] to exit", False, (0, 0, 0))
    msg_instructions3 = small_font.render("Press [n] for new game", False, (0, 0, 0))
    screen.blit(msg_instructions3, (600, 340))
    screen.blit(msg_instructions1, (600, 360))
    screen.blit(msg_instructions2, (600, 380))

    if player != None and dealer != None:
        # update player funds and bet
        msg_score = small_font.render("Player score: " + str(player.get_score()), False, (0, 0, 0))
        msg_bet = small_font.render("Player bet: " + str(bet), False, (0, 0, 0))
        screen.blit(msg_score, (600, 10))
        screen.blit(msg_bet, (600, 30))
        # update dealer and player cards
        dealer.display_cards(deck, state)
        player.display_cards(deck)

    # update dynamic instructions
    if state == 0:
        # would you like to start a new game?
        msg_game = small_font.render(MSG_DEAL, False, (0, 0, 0))
    elif state == 3:
        # during the player's turn...
        msg_game = small_font.render(MSG_HIT_OR_STAND, False, (0, 0, 0))
    elif state >= 5 and state < 6:
        # outcome of the round...
        if state == 5.1:
            # player wins
            msg_game = small_font.render(MSG_PLAYER_WINS, False, (0, 0, 0))
        elif state == 5.2:
            # dealer wins
            msg_game = small_font.render(MSG_DEALER_WINS, False, (0, 0, 0))
        elif state == 5.3:
            # player bust
            msg_game = small_font.render(MSG_PLAYER_BUST, False, (0, 0, 0))
        elif state == 5.4:
            # dealer bust
            msg_game = small_font.render(MSG_DEALER_BUST, False, (0, 0, 0))
        else:
            # draw hand
            msg_game = small_font.render(MSG_DRAW, False, (0, 0, 0))
    else:
        msg_game = small_font.render(" ", False, (0, 0, 0))
    screen.blit(msg_game, (20, 340))

    # refresh the display
    pygame.display.update()

def main():
    global state

    while True:
        # event handlers
        for event in pygame.event.get():
            if event.type == KEYDOWN and state > 1:
                key_down(event, player, deck)
            elif event.type == KEYDOWN and state <= 1:
                key_down(event)
        # update display
        if state > 1:
            update_display(state, player, dealer, deck)
        else:
            update_display(state)
        pygame.display.update()

        # create new game elements
        if state == 1:
            # Create the deck and shuffle it
            deck = CardDeck()
            deck.load_card_images()
            deck.shuffle()
            # Create dealer and player
            player = Player()
            dealer = Dealer()
            # game ready to start
            state += 1

        # start a new hand
        if state == 2:
            # deal
            player.bet()
            deal(deck, dealer, player)
            # player goes first
            state += 1

        # player's turn
        if state == 3:
            while player.get_count(deck) < 21 and state == 3:
                # event handlers
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        key_down(event, player, deck)
                # update display
                update_display(state, player, dealer, deck)
                pygame.display.update()
                clock.tick(30)
            if player.get_count(deck) > 21:
                state = 5
            if player.get_count(deck) == 21:
                state = 4

        # dealer's turn
        if state == 4:
            dealer.update(deck)

        # decide outcome of round
        if state >= 5:
            # work out who won
            if player.get_count(deck) > dealer.get_count(deck):
                if player.get_count(deck) <= 21:
                    # player won
                    player.scored()                # Fix here
                    state = 5.1
                else:
                    # player bust
                    state = 5.3
            elif player.get_count(deck) < dealer.get_count(deck):
                if dealer.get_count(deck) <= 21:
                    # dealer won
                    state = 5.2
                else:
                    # dealer bust
                    player.scored()
                    state = 5.4
            elif player.get_count(deck) == dealer.get_count(deck):
                # draw hand
                player.scored(1)
                state = 5.5
            print(player.update())
            clock.tick(30)


if __name__ == '__main__':
    main()
