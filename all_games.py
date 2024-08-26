from colorama import just_fix_windows_console
from colorama import init, Fore, Style, Back
from rock_paper_scissors import main
from tic_tac_toe import tic_tac_toe
from blackjack import blackjack
from termcolor import colored
from rich import print as pr
from Hangman import hangman
from game import game
import pyfiglet
import winsound
import pyttsx3

just_fix_windows_console()
init()
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak_greeting():
    print("\n")
    greeting = "Welcome to the gaming portal."
    print(colored(greeting, 'white', 'on_red'))
    engine.say(greeting)
    engine.runAndWait()

def display_title(title):
    print("\n")
    winsound.PlaySound('notification.wav', winsound.SND_ALIAS)
    title = pyfiglet.figlet_format('Gaming Portal', font='slant')
    pr(f'[magenta]{title}[/magenta]')

# Menu
def menu():
    speak_greeting()
    print("\n")
    display_title('Welcome to gaming portal')
    while True:
        print('All Games')
        print(Back.GREEN )
        print(Fore.GREEN + '1. Hangman' + Style.RESET_ALL)
        print(Fore.BLUE + '2. Rock paper Scissors' + Style.RESET_ALL)
        print(Fore.YELLOW + '3. Quiz Game' + Style.RESET_ALL)
        print(Fore.GREEN + '4. Tic Tac Toe' + Style.RESET_ALL)
        print(Fore.BLUE + '5. Blackjack' + Style.RESET_ALL)
        print(Fore.RED + '6. Exit Gaming Portal' + Style.RESET_ALL)

        try: 
            choice = int(input("Enter your choice (1-6): "))
            if choice == 1:
                print('Hangman Game')
                hangman.hangman(engine)
            elif choice == 2:
                print('Rock paper Scissors Game')
                main.user_options(engine)
            elif choice == 3:
                print('Quiz Game')
                game.user_options()
            elif choice == 4:
                print('Tic Tac Toe')
                obj_tictactoe = tic_tac_toe.TicTacToe()
                obj_tictactoe.play()
            elif choice == 5:
                print('Blackjack')
                obj_blackjack = blackjack.Blackjack()
                obj_blackjack.play()
            elif choice == 6:
                print("Exiting...")
                engine.say("Exiting. Thank you for playing!")
                engine.runAndWait()
                break
            else:
                print(Fore.RED + 'Invalid Choice. Please enter a number between 1 and 4.' + Style.RESET_ALL)
        except ValueError as e:
            print("Only integers are allowed", e)

menu()
