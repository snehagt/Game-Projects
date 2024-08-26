import os
import time
import random
import pyttsx3
import winsound
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()
    
def init_text_to_speech():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # You can change the voice here if needed
    return engine

# Define the ASCII art for the hangman stages
hangman_stages = [
    """
     ------
    |    |
    |
    |
    |
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |
    |
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |    |
    |
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |   /|
    |
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |   /|\\
    |
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |   /|\\
    |   /
    |
    --------
    """,
    """
     ------
    |    |
    |    O
    |   /|\\
    |   / \\
    |
    --------
    """
]

# Define the list of words to choose from
words = ["hangman", "python", "computer", "keyboard", "science", "programming"]

# Define sound files
SOUND_START = "hangman_start.wav"
SOUND_CORRECT_GUESS = "correct_guess.wav"
SOUND_INCORRECT_GUESS = "incorrect_guess.wav"
SOUND_WIN = "hangman_win.wav"
SOUND_LOSE = "hangman_lose.wav"

# Function to play sound with proper timing
def play_sound(sound_file, delay=0):
    winsound.PlaySound(sound_file, winsound.SND_ASYNC)
    time.sleep(delay)

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to select word
def select_word(words):
    return random.choice(words)

# Function to display word
def display_word(word, guessed_letters):
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display

# Function to display hangman stage
def display_hangman(incorrect_guesses):
    print(Fore.RED + hangman_stages[incorrect_guesses])

# Function to display colored message
def display_message(message, color):
    print(color + message)

# Function to display user instructions
def display_instructions():
    print("\n")
    print(Fore.YELLOW + "███████╗██╗   ██╗██████╗ ██╗     ███████╗██████╗ ███████╗" + Style.RESET_ALL)
    print(Fore.YELLOW + "██╔════╝██║   ██║██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝" + Style.RESET_ALL)
    print(Fore.YELLOW + "███████╗██║   ██║██████╔╝██║     █████╗  ██████╔╝███████╗" + Style.RESET_ALL)
    print(Fore.YELLOW + "╚════██║██║   ██║██╔═══╝ ██║     ██╔══╝  ██╔══██╗╚════██║" + Style.RESET_ALL)
    print(Fore.YELLOW + "███████║╚██████╔╝██║     ███████╗███████╗██║  ██║███████║" + Style.RESET_ALL)
    print(Fore.YELLOW + "╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝" + Style.RESET_ALL)
    print("\n")
    print(Fore.GREEN + "Welcome to Hangman!" + Style.RESET_ALL)
    print(Fore.GREEN + "Guess the word by entering one letter at a time." + Style.RESET_ALL)
    print(Fore.GREEN + "You have 6 incorrect guesses before the hangman is complete." + Style.RESET_ALL)
    print(Fore.YELLOW + "Let's start!" + Style.RESET_ALL)

# Function to play hangman game
def hangman(engine):
    winsound.PlaySound('notification.wav', winsound.SND_ALIAS)
    speak(engine, "Initializing...")
    speak(engine, "Welcome to Hangman...")
    display_instructions()
    
    # Wait for the user to press Enter to start the game
    input("Press Enter to start...")
    while True:
        clear_screen()
        play_sound(SOUND_START)
        word = select_word(words)
        guessed_letters = []
        incorrect_guesses = 0

        while incorrect_guesses < len(hangman_stages) - 1:
            clear_screen()
            display_hangman(incorrect_guesses)
            print(display_word(word, guessed_letters))

            guess = input("Guess a letter: ").lower()
            if len(guess) != 1 or not guess.isalpha():
                display_message("Please enter a single letter.", Fore.RED)
                time.sleep(2)
                continue

            if guess in guessed_letters:
                display_message("You already guessed that letter.", Fore.RED)
                time.sleep(2)
                continue

            guessed_letters.append(guess)

            if guess not in word:
                display_message("Incorrect guess!", Fore.RED)
                play_sound(SOUND_INCORRECT_GUESS)
                time.sleep(1)
                incorrect_guesses += 1
            else:
                display_message("Correct guess!", Fore.GREEN)
                play_sound(SOUND_CORRECT_GUESS)
                time.sleep(1)

            if all(letter in guessed_letters for letter in word):
                clear_screen()
                display_hangman(incorrect_guesses)
                print(display_word(word, guessed_letters))
                display_message("Congratulations, you guessed the word!", Fore.GREEN)
                play_sound(SOUND_WIN, 2)
                break

        else:
            clear_screen()
            display_hangman(incorrect_guesses)
            display_message("Sorry, you ran out of guesses. The word was: " + word, Fore.RED)
            play_sound(SOUND_LOSE, 2)

        time.sleep(3)

        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            display_message("Thanks for playing!", Fore.YELLOW)
            break
