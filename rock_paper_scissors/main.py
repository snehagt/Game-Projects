import random
import pyttsx3
import winsound

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def game(user_choice, computer_choice):
    if user_choice == computer_choice:
        print("Game ties! No one wins. Try again")
    elif ((user_choice == 1 and computer_choice == 2) or \
            (user_choice == 2 and computer_choice == 3) or \
            (user_choice == 3 and computer_choice == 1)):
            print('You Lose!')
    else:
            print('You win!')

def user_input():
    user_choice = int(input("Enter your choice: "))
    computer_choice = random.randint(1, 3)
    return user_choice, computer_choice

def user_options(engine): 
    display_title()
    winsound.PlaySound('notification.wav', winsound.SND_ALIAS)
    speak(engine, "Welcome to Rock paper scissors...")
    print("Welcome to Rock-Paper-Scissors! Let's start")
    print('Press 1 for Rock, 2 for Paper, 3 for Scissors')
    while True:
        user_choice, computer_choice = user_input()
        game(user_choice, computer_choice)
        play_again = input("Do you want to play again? (yes/no): ").lower()
        speak(engine, "Do you want to play again?")
        if play_again != 'yes':
            break

def display_title():
    print("\n")
    print("██████╗ ██╗   ██╗███████╗██████╗ ██╗███╗   ██╗ ██████╗ ")
    print("██╔══██╗██║   ██║██╔════╝██╔══██╗██║████╗  ██║██╔════╝ ")
    print("██████╔╝██║   ██║█████╗  ██████╔╝██║██╔██╗ ██║██║  ███╗")
    print("██╔══██╗██║   ██║██╔══╝  ██╔══██╗██║██║╚██╗██║██║   ██║")
    print("██████╔╝╚██████╔╝███████╗██║  ██║██║██║ ╚████║╚██████╔╝")
    print("╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ")
    print("\n")