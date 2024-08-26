import random
import winsound
from colorama import Fore, Style

class Blackjack:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # 11 represents Ace
        self.player_hand = []
        self.dealer_hand = []
        self.achievements = {"Win 5 games": False, "Win with a Blackjack": False}
        self.wins = 0

    def deal_card(self):
        return self.deck.pop(random.randint(0, len(self.deck)-1))

    def calculate_score(self, hand):
        score = sum(hand)
        if score > 21 and 11 in hand:
            hand.remove(11)
            hand.append(1)
            score = sum(hand)
        return score

    def display_game(self, player_score, dealer_score, player_busted=False, dealer_busted=False):
        print("\n")
        print(Fore.GREEN + "Player's Hand:" + Style.RESET_ALL, self.player_hand, "(Score:", player_score, ")")
        print(Fore.RED + "Dealer's Hand:" + Style.RESET_ALL, self.dealer_hand, "(Score:", dealer_score, ")")
        if player_busted:
            print(Fore.RED + "Player Busted! Dealer wins." + Style.RESET_ALL)
        elif dealer_busted:
            print(Fore.GREEN + "Dealer Busted! Player wins." + Style.RESET_ALL)
        print("\n")

    def display_title(self):
        print("\n")
        print(Fore.YELLOW + "███████╗██╗   ██╗██████╗ ██╗     ███████╗██████╗ ███████╗" + Style.RESET_ALL)
        print(Fore.YELLOW + "██╔════╝██║   ██║██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝" + Style.RESET_ALL)
        print(Fore.YELLOW + "███████╗██║   ██║██████╔╝██║     █████╗  ██████╔╝███████╗" + Style.RESET_ALL)
        print(Fore.YELLOW + "╚════██║██║   ██║██╔═══╝ ██║     ██╔══╝  ██╔══██╗╚════██║" + Style.RESET_ALL)
        print(Fore.YELLOW + "███████║╚██████╔╝██║     ███████╗███████╗██║  ██║███████║" + Style.RESET_ALL)
        print(Fore.YELLOW + "╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝" + Style.RESET_ALL)
        print("\n")
        winsound.PlaySound('notification.wav', winsound.SND_ALIAS)


    def display_tutorial(self):
        print("Welcome to Blackjack! Here's a quick tutorial:")
        print("- You will be dealt two cards initially.")
        print("- The dealer will also be dealt one card face up.")
        print("- Your goal is to get as close to 21 as possible without going over.")
        print("- You can 'Hit' to draw another card or 'Stand' to keep your current hand.")
        print("- If your total exceeds 21, you bust and lose the round.")
        print("- If the dealer busts or your hand is higher than the dealer's, you win.")
        print("- If both you and the dealer have the same score, it's a tie.")
        print("\n")

    def check_achievements(self):
        if self.wins == 5 and not self.achievements["Win 5 games"]:
            self.achievements["Win 5 games"] = True
            print(Fore.GREEN + "Congratulations! You've unlocked the 'Win 5 games' achievement!" + Style.RESET_ALL)
        if 11 in self.player_hand and 10 in self.player_hand and len(self.player_hand) == 2 and not self.achievements["Win with a Blackjack"]:
            self.achievements["Win with a Blackjack"] = True
            print(Fore.GREEN + "Congratulations! You've unlocked the 'Win with a Blackjack' achievement!" + Style.RESET_ALL)

    def play(self):
        self.display_title()
        self.display_tutorial()

        while True:
            self.player_hand = [self.deal_card(), self.deal_card()]
            self.dealer_hand = [self.deal_card()]

            player_score = self.calculate_score(self.player_hand)
            dealer_score = self.calculate_score(self.dealer_hand)

            self.display_game(player_score, dealer_score)

            while player_score < 21:
                action = input("Do you want to Hit or Stand? (h/s): ").lower()
                if action == 'h':
                    self.player_hand.append(self.deal_card())
                    player_score = self.calculate_score(self.player_hand)
                    self.display_game(player_score, dealer_score)
                    if player_score > 21:
                        self.display_game(player_score, dealer_score, player_busted=True)
                        break
                elif action == 's':
                    break

            while dealer_score < 17:
                self.dealer_hand.append(self.deal_card())
                dealer_score = self.calculate_score(self.dealer_hand)
                self.display_game(player_score, dealer_score)

            if dealer_score > 21:
                self.display_game(player_score, dealer_score, dealer_busted=True)
                print(Fore.GREEN + "Player wins!" + Style.RESET_ALL)
                self.wins += 1
            elif player_score > dealer_score:
                self.display_game(player_score, dealer_score)
                print(Fore.GREEN + "Player wins!" + Style.RESET_ALL)
                self.wins += 1
            elif player_score < dealer_score:
                self.display_game(player_score, dealer_score)
                print(Fore.RED + "Dealer wins!" + Style.RESET_ALL)
            else:
                self.display_game(player_score, dealer_score)
                print("It's a tie!")

            self.check_achievements()

            play_again = input("Do you want to play again? (y/n): ").lower()
            if play_again != 'y':
                print("Thanks for playing!")
                break
