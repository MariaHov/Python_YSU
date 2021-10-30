import itertools
import random
from abc import ABC, abstractmethod
class BlackJackCardABC(ABC):
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def value(self):
        pass

class BlackjackCard(BlackJackCardABC):
    suits = ['♠', '♣', '♥', '⬥']
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']

    def __repr__(self):
        return f'| {self.suit} of {self.rank} |'

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class BlackjackFaceCard(BlackjackCard):
    ranks = ['J', 'Q', 'K']

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    def value(self):
        if (self.rank in self.ranks):
            return 10


class BlackjackNumCard(BlackjackCard):
    ranks = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    def value(self):
        return self.ranks[self.rank - 2]


class BlackjackAceCard(BlackjackCard):
    ranks = ['A']

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

    def value(self):
        if (self.rank in self.ranks):
            return (1, 11)

class BlackJackDeckABC(ABC):
    @abstractmethod
    def create_deck(self):
        pass

    @abstractmethod
    def shuffle(self):
        pass

class BlackJackDeck(BlackJackDeckABC):
    def __init__(self):
        self.deck_ = []
        self.create_deck()

    def create_deck(self):
        deck1 = [BlackjackFaceCard(suit, rank) for suit in BlackjackFaceCard.suits for rank in BlackjackFaceCard.ranks]
        deck2 = [BlackjackNumCard(suit, rank) for suit in BlackjackNumCard.suits for rank in BlackjackNumCard.ranks]
        deck3 = [BlackjackAceCard(suit, rank) for suit in BlackjackAceCard.suits for rank in BlackjackAceCard.ranks]
        self.deck_ = deck1 + deck2 + deck3
        return self.deck_

    def shuffle(self):
        return random.sample(self.deck_, len(self.deck_))

    @staticmethod
    def deal(deck):
        return deck.pop()



class BlackJack_player:

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.hard = 0
        self.soft = 0
        self.win = 0
    def __repr__(self):
        return f'{self.name} {self.hand})'


class BlackJack_game:

    max_players = 5;

    def __init__(self, deck):
        self.deck = deck
        self.number_of_players = 0
        self.players = []
        self.dealer_cards = 0
        self.initial_deck = 0
        self.dealer = 0
        self.flag = []
    def add_player(self):
        while (self.number_of_players < self.max_players):
          #  print("Do you want to add a player?(y/n)")
            yn = input("Do you want to add a player?(y/n) ")
            if ((yn == 'n') & (self.number_of_players == 0)):
                print("we don't have enought players")
                return self.add_player()
            elif (yn == 'y'):
                player = BlackJack_player(input("Please enter the player's name: "))
                self.number_of_players += 1
                self.players.append(player.name)
                print(f'{player.name} added!')
                if (self.number_of_players == self.max_players):
                    print('You reached maximum players')
                    print('-----------------------------------')
                    break
                else:
                    return self.add_player()
            elif (yn == 'n'):
                print('-----------------------------------')
                break
            else:
                print("Please enter 'y' or 'n'")
                return self.add_player()

    def initial_deal(self):
        print("Starting the game")
        player_dict = {f'{key}': [] for key in self.players}
        dealer_dict = {'Dealer': []}
        dealer_dict['Dealer'].append(self.deck.pop())
        for key in player_dict:
            player_dict[key].append(self.deck.pop())

        dealer_dict['Dealer'].append(self.deck.pop())
        self.dealer_cards = [dealer_dict['Dealer'][0], dealer_dict['Dealer'][1]]
        # print(self.dealer_hidden_card)
        dealer_dict['Dealer'][1] = '| <card hidden> |'
        for key in player_dict:
            player_dict[key].append(self.deck.pop())
        dealer_dict.update(player_dict)
        for key in dealer_dict:
            print('\n')
            print(key, end=':')
            for i in range(len(dealer_dict[key])):
                print(dealer_dict[key][i], end=' ')
        self.initial_deck = player_dict
        print()
        return ('-----------------------------------')

    #     def initial_deal(self):
    #         print("Starting the game")
    #         self.dealer = BlackJack_player('Dealer')
    #         print(self.dealer)
    #         self.dealer.hand.append(self.deck.pop())
    #         for i in range(len(self.players)):
    #              a = self.deck.pop()
    #              self.players[i].hand = self.players[i].hand+a
    #              print(self.players[i])
    #         print(self.dealer)

    def check_hand(self, hand):
        soft = 0
        hard = 0
        sum = 0
        checker = []
        for i in range(len(hand)):
            checker.append(hand[i].rank)
        if 'A' not in checker:
            for i in range(len(hand)):
                sum += hand[i].value()
            return sum
        else:
            for i in range(len(hand)):
                if (hand[i].rank == 'A'):
                    soft += 1
                    hard += 11
                else:
                    soft += hand[i].value()
                    hard += hand[i].value()
            return (soft, hard)

    def ask_user(self, player='name'):
        print(player, ':', self.initial_deck[player])
        checker = []
        hand = self.initial_deck[player]
        for i in range(len(hand)):
            checker.append(hand[i].rank)
        if 'A' not in checker:
            total = self.check_hand(hand)
            print(f'your total is {total}')
        else:
            soft, hard = self.check_hand(hand)
            print(f'your sums are - soft: {soft}, hard:{hard}')
        try:
            if (total < 21):
                a = input("Do you want another card? (y/n): ")
                if (a == 'y'):
                    self.initial_deck[player].append(self.deck.pop())
                    return self.ask_user(player)
                else:
                    return total
            elif (total == 21):
                print('BlackJack!!! you win!!')
                return 100
            else:
                print('you bust(((')
                return 0
        except:
            # ete ystex enq mtel uremn soft hard unenq
            if (soft == 21 or hard == 21):
                print('BlackJack!!! you win!!')
                return 100
            elif (soft > 21):
                print('You bust((((')
                return 0
            elif (soft < 21):
                a = input("Do you want another card? (y/n): ")
                if (a == 'y'):
                    self.initial_deck[player].append(self.deck.pop())
                    return self.ask_user(player)
                else:
                    if (hard < 21):
                        return hard
                    else:
                        return soft

    def all_players(self):

        self.flag = self.players.copy()
        for i in range(len(self.players)):
            print('')
            print(f'playing with {self.players[i]}')
            self.flag[i] = self.ask_user(self.players[i])

    def ask_dealer(self):
        checker = []
        print('Dealer :', self.dealer_cards)
        for i in range(len(self.dealer_cards)):
            checker.append(self.dealer_cards[i].rank)
        if 'A' not in checker:
            print('Dealers Total is ', self.check_hand(self.dealer_cards))
            if (self.check_hand(self.dealer_cards) < 17):
                self.dealer_cards.append(self.deck.pop())
                return self.ask_dealer()
            elif (self.check_hand(self.dealer_cards) > 16 and self.check_hand(self.dealer_cards) < 21):
                for i in range(len(self.flag)):
                    if ((self.check_hand(self.dealer_cards)) > (self.flag[i])):
                        self.flag[i] = 'you bust'
                    elif (self.check_hand(self.dealer_cards) == self.flag[i]):
                        self.flag[i] = 'and dealer are friends :)'
                    else:
                        self.flag[i] = 'You win!!!'
            else:
                print("Dealer bust!!!")
                for i in range(len(self.flag)):
                    if (self.flag[i] == 0):
                        self.flag[i] = 'You have lost('
                    else:
                        self.flag[i] = 'You win'
        else:
            soft, hard = self.check_hand(self.dealer_cards)
            print(f'your sums are - soft: {soft}, hard:{hard}')
            if (soft > 21):
                print("Dealer bust!!!")
                for i in range(len(self.flag)):
                    if (self.flag[i] == 0):
                        self.flag[i] = 'You have lost('
                    else:
                        self.flag[i] = 'You win'
            elif (soft > 16 and soft <= 21):
                # nkatenq vor ete stex enq mtel uremn hardy hastat shat metsa
                for i in range(len(self.flag)):
                    if (soft > (self.flag[i])):
                        self.flag[i] = 'you bust'
                    elif (soft == self.flag[i]):
                        self.flag[i] = 'and dealer are friends :)'
                    else:
                        self.flag[i] = 'You win!!!'
            elif (soft <= 16):
                self.dealer_cards.append(self.deck.pop())
                return self.ask_dealer()

    def winners(self):
        for i in range(len(self.flag)):
            print(self.players[i], self.flag[i])

    @staticmethod
    def start_again():
        a = input("Do you wanna start again? (y/n) ")
        if (a=='y' or a=='n'):
            return a
        else:
            print("please enter 'y' or 'n'")
            return BlackJack_game.start_again()


def main():
    def looping():
        deck = BlackJackDeck()
        shuffled_deck = deck.shuffle()
        my_game = BlackJack_game(shuffled_deck)
        my_game.add_player()
        a = my_game.initial_deal()
        print(a)
        my_game.all_players()
        a = my_game.ask_dealer()
        my_game.winners()
        if(my_game.start_again() == 'y'):
            looping()
        else:
            print('Game is over')
    looping()

main()

