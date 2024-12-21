import random

class Blackjack:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        self.player_hand = []
        self.dealer_hand = []

    def deal_card(self, hand):
        card = random.choice(self.deck)
        self.deck.remove(card)
        hand.append(card)
        return card

    def calculate_hand(self, hand):
        total = sum(hand)
        aces = hand.count(11)
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def start_game(self):
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]
        return self.player_hand, self.dealer_hand

    def player_hit(self):
        return self.deal_card(self.player_hand)

    def dealer_play(self):
        while self.calculate_hand(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)

    def get_winner(self):
        player_total = self.calculate_hand(self.player_hand)
        dealer_total = self.calculate_hand(self.dealer_hand)
        
        if player_total > 21:
            return "Dealer wins! You busted.", 3
        elif dealer_total > 21:
            return "You win! Dealer busted.", 4
        elif player_total > dealer_total:
            return "You win!", 1
        elif player_total < dealer_total:
            return "Dealer wins!", 2
        else:
            return "It's a tie!", 0

