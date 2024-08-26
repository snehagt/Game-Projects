import pyttsx3
import winsound
from colorama import Fore, Style

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.achievements = {"Win 5 games": False}
        self.wins = {"X": 0, "O": 0}
        self.engine = pyttsx3.init()

    def display_title(self):
        print("\n")
        print(Fore.YELLOW + "██╗    ██╗██╗███████╗██╗  ██╗    ████████╗ ██████╗ ██████╗ ██╗  ██╗" + Style.RESET_ALL)
        print(Fore.YELLOW + "██║    ██║██║██╔════╝██║ ██╔╝    ╚══██╔══╝██╔═══██╗██╔══██╗██║ ██╔╝" + Style.RESET_ALL)
        print(Fore.YELLOW + "██║ █╗ ██║██║███████╗█████╔╝        ██║   ██║   ██║██████╔╝█████╔╝ " + Style.RESET_ALL)
        print(Fore.YELLOW + "██║███╗██║██║╚════██║██╔═██╗        ██║   ██║   ██║██╔═══╝ ██╔═██╗ " + Style.RESET_ALL)
        print(Fore.YELLOW + "╚███╔███╔╝██║███████║██║  ██╗       ██║   ╚██████╔╝██║     ██║  ██╗" + Style.RESET_ALL)
        print(Fore.YELLOW + " ╚══╝╚══╝ ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝ ╚═╝     ╚═╝  ╚═╝" + Style.RESET_ALL)
        print("\n")
        winsound.PlaySound('notification.wav', winsound.SND_ALIAS)

    def display_game(self):
        print("\n")
        print(" " + self.board[0] + " | " + self.board[1] + " | " + self.board[2] + " ")
        print("---|---|---")
        print(" " + self.board[3] + " | " + self.board[4] + " | " + self.board[5] + " ")
        print("---|---|---")
        print(" " + self.board[6] + " | " + self.board[7] + " | " + self.board[8] + " ")
        print("\n")

    def check_winner(self):
        for choice in range(0, 9, 3):
            if self.board[choice] == self.board[choice+1] == self.board[choice+2] != " ":
                return self.board[choice]

        for choice in range(3):
            if self.board[choice] == self.board[choice+3] == self.board[choice+6] != " ":
                return self.board[choice]

        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]

        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]

        if " " not in self.board:
            return "Tie"

        return None

    def check_achievements(self):
        if self.wins[self.current_player] == 5 and not self.achievements["Win 5 games"]:
            self.achievements["Win 5 games"] = True
            self.engine.say(Fore.GREEN + f"Congratulations! Player {self.current_player} unlocked the 'Win 5 games' achievement!" + Style.RESET_ALL)
            self.engine.runAndWait()

    def announce_winner(self, winner):
        if winner == "Tie":
            print(Fore.RED + "It's a tie!" + Style.RESET_ALL)
            self.engine.say("It's a tie!")
        else:
            print(Fore.GREEN + f"Player {winner} wins!" + Style.RESET_ALL)
            self.engine.say(f"Player {winner} wins!" + Style.RESET_ALL)
        self.engine.runAndWait()

    def play(self):
        self.display_title()
        print(Fore.YELLOW+ "Welcome to Tic Tac Toe!" + Style.RESET_ALL)
        self.display_game()
        
        while True:
            choice = int(input(Fore.GREEN + f"Player {self.current_player}, enter your move (1-9): " + Style.RESET_ALL)) - 1

            if 0 <= choice <= 8 and self.board[choice] == " ":
                self.board[choice] = self.current_player
                self.display_game()

                winner = self.check_winner()
                if winner:
                    self.announce_winner(winner)
                    if winner != "Tie":
                        self.wins[winner] += 1
                    self.check_achievements()
                    break

                self.current_player = "O" if self.current_player == "X" else "X"
            else:
                print(Fore.RED + "Invalid move! Please select an empty position between 1 and 9." + Style.RESET_ALL)
            