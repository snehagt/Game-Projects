import os
import time
import json
import random
import string
import pyttsx3
import winsound
import threading
from termcolor import colored
from .questions import questions
from .instructions import Instructions
from colorama import init, Fore, Style, Back
from colorama import just_fix_windows_console
from .users import users, add_user, show_users, save_users_data, load_users_data

init()
# Initialize users data
users = load_users_data()

# Lifelines dictionary to track lifelines used by each user
lifelines_used = {}

# Function to save lifelines data
def save_lifelines_data():
    with open('lifelines_data.json', 'w') as file:
        json.dump(lifelines_used, file)

# Load lifelines data
try:
    with open('lifelines_data.json', 'r') as file:
        lifelines_used = json.load(file)
except FileNotFoundError:
    lifelines_used = {}

def display_questions(questions, ques_number):
    shuffled_questions = list(questions.keys())
    random.shuffle(shuffled_questions)

    shuffled_question = shuffled_questions[0]
    choices = questions[shuffled_question]
    correct_answer = choices[0]
    random.shuffle(choices)

    # Print question in red
    print(Fore.RED + f'{ques_number}. {shuffled_question}:')
    for i, choice in enumerate(choices, start=1):
        # Print choices in green
        print(Fore.GREEN + f'   {string.ascii_uppercase[i-1]}. {choice}')
    print(Style.RESET_ALL)  # Reset color after printing

    return shuffled_question, choices, correct_answer

# Function to get user's answer
def get_answer():
    while True:
        ans = input("Enter your choice (or 'L' to activate lifeline): ").strip().upper()  # Strip whitespace and convert to uppercase
        if ans == 'L':
            return ans  # Return 'L' to indicate lifeline activation
        elif ans in string.ascii_uppercase:
            return ans
        else:
            speak(engine, "Invalid choice. Please enter a valid option.")
            print("Invalid choice. Please enter a valid option.")

# Function to calculate amount won/lost by user
def calculate_user_amount(user, question_number, answer, shuffled_choices, correct_answer):
    global users 
    question_number = int(question_number)
    if user not in users:
        print("Creating a new user.")
        add_user(user)
        users = load_users_data()
    amount = 0  # Initialize amount variable
    if shuffled_choices[ord(answer) - 65] == correct_answer:
        if 1 <= question_number <= 5:
            amount = 5000
        elif 6 <= question_number <= 10:
            amount = 15000
    users[user] += amount
    save_users_data(users)
    return amount

def lifeline_50_50(choices, correct_answer):
    incorrect_choices = [choice for choice in choices if choice != correct_answer]
    choices_to_remove = random.sample(incorrect_choices, len(incorrect_choices) - 1)
    for choice in choices_to_remove:
        choices.remove(choice)
    return choices

# Function to use double dip lifeline
def lifeline_double_dip(user, i, question, choices, correct_answer):
    print(f'You have activated Double Dip lifeline. You have 2 attempts to answer the question.')
    for attempt in range(2):
        print(f'Attempt {attempt + 1}:')
        answer = get_answer()
        if choices[ord(answer) - 65] == correct_answer:
            print(f'Correct answer! You win {attempt + 1} times the original amount.')
            amount = calculate_user_amount(user, i, answer, choices, correct_answer) * (attempt + 1)
            return amount
        else:
            print(f'Wrong answer! You have 1 attempt left.')
    print('You have used both attempts. The correct answer was', correct_answer)
    return 0

# Function to use flip the question lifeline
def lifeline_flip_the_question():
    print('You have activated Flip the Question lifeline. The current question will be skipped.')

def play_beep_sound():
    while True:
        winsound.Beep(1000, 500)  # Play beep sound
        time.sleep(1)  # Wait for 1 second between each beep

# Function to start the timer
def start_timer(timer_stop_event, user, amount_till_question, ques_num):
    while not timer_stop_event.is_set():
        for remaining in range(30, 0, -1):
            if timer_stop_event.is_set():
                return  # Exit the function if the timer stop event is set
            if remaining <= 5:
                threading.Thread(target=play_beep_sound).start()  # Play beep sound in a separate thread
            time.sleep(1)
        if not timer_stop_event.is_set():
            print("\nTime's up!")
            print(f"Your total amount till question {ques_num} is {amount_till_question} Rs.")
            print("You lose!")
            os._exit(1)  # Terminate the program abruptly
def play_background_music():
    winsound.PlaySound("background_music.wav", winsound.SND_FILENAME | winsound.SND_LOOP | winsound.SND_ASYNC)

# Function to play the game
def play_game(user):
    threading.Thread(target=play_background_music).start()
    total_amount = 0  # Initialize total amount
    amount_till_5th_question = 0  # Initialize amount till 5th question
    available_lifelines = ['50/50', 'Double Dip', 'Flip the Question']  # Available lifelines for each user
    used_lifelines = lifelines_used.get(user, [])  # Lifelines used by the user
    for i in range(1, len(questions) + 1):
        shuffled_question, shuffled_choices, correct_answer = display_questions(questions, i)
        timer_stop_event = threading.Event()
        timer_thread = threading.Thread(target=start_timer, args=(timer_stop_event, user, amount_till_5th_question, i))
        timer_thread.start()
        answer_given = False  # Flag to track if the user has given an answer
        while not answer_given:
            answer = get_answer()
            answer_given = True  # Set the flag to indicate that an answer has been given
            timer_stop_event.set()  # Set the timer stop event to interrupt the timer thread
        timer_thread.join()
        print("\n")  # Move to the next line after the timer stops
        if answer == 'L':
            if not available_lifelines:
                print("You have already used all available lifelines.")
                continue

            print("\nAvailable Lifelines:")
            for index, lifeline in enumerate(available_lifelines, start=1):
                print(f"{index}. {lifeline}")

            lifeline_choice = input("Enter the number corresponding to the lifeline you want to use: ").strip()
            if lifeline_choice not in ['1', '2', '3']:
                print("Invalid input. Please enter the number corresponding to the lifeline you want to use.")
                continue

            lifeline_index = int(lifeline_choice) - 1
            chosen_lifeline = available_lifelines[lifeline_index]

            if chosen_lifeline in used_lifelines:
                print("You have already used this lifeline.")
                continue

            used_lifelines.append(chosen_lifeline)
            lifelines_used[user] = used_lifelines
            available_lifelines.remove(chosen_lifeline)

            if chosen_lifeline == '50/50':
                lifeline_50_50(shuffled_choices, correct_answer)
            elif chosen_lifeline == 'Double Dip':
                amount = lifeline_double_dip(user, i, shuffled_question, shuffled_choices, correct_answer)
                total_amount += amount
            elif chosen_lifeline == 'Flip the Question':
                lifeline_flip_the_question()

            continue 

        amount = calculate_user_amount(user, i, answer, shuffled_choices, correct_answer)
        total_amount += amount  # Update total amount
        if 1 <= i <= 5:
            amount_till_5th_question += amount  # Update amount till 5th question
        if amount > 0:
            print(f"Correct answer! You win {amount} Rs.")
        else:
            print(f"Wrong answer. You lose! Your total amount is {amount_till_5th_question} Rs.")
            exit()

        save_users_data(users)

        if i >= 6 and amount == 0:  # If the answer is wrong between 6th and 10th question
            print(f"Sorry, your total amount is {amount_till_5th_question} Rs. You lose!")
            exit()

        save_lifelines_data()  # Save lifelines data after each question
        print()

    print(f"Congratulations! You won the game. Your total amount is {total_amount} Rs.")

def play_sound():
    winsound.PlaySound("sound.wav", winsound.SND_FILENAME)

def init_text_to_speech():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can change the voice here if needed
    return engine

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

# use Colorama to make Termcolor work on Windows too
just_fix_windows_console()

def character_user():
    frames = [
        "      .--..--..--..--..--..--.",
        "    .' \  (`._   (_)     _   \\",
        "  .'    |  '._)         (_)  |",
        "  \\ _.')\\      .----..---.   /",
        "  |(_.'  |    /    .-\\-.  \\  |",
        "  \\     0|    |   ( O| O) | o|",
        "   |  _  |  .--.____.'._.-.  |",
        "   \\ (_) | o         -` .-`  |",
        "    |    \\   |`-._ _ _ _ _\\ /",
        "    \\    |   |  `. |_||_|   |",
        "    | o  |    \\_      \\     |     -.   .-.  Welcome To the Quiz Gaming Pad! ",
        "    |.-.  \\     `--..-'   O |     `.`-' .'",
        "  _.'  .' |     `-.-'      /-.__   ' .-'",
        ".' `-.` '.|='=.='=.='=.='=|._/_ `-'.`",
        "`-._  `.  |________/\\_____|    `-.`",
        "   .'   ).| '=' '='\\/ '=' |",
        "   `._.`  '---------------'",
        "           //___\\   //___\\",
        "             ||       ||",
        "             ||_.-.   ||_.-.",
        "            (_.--__) (_.--__)",
    ]
    print("\033[H\033[J", end='', flush=True)
    for frame in frames:
        colored_frame = ""
        for char in frame:
            if char == ".":
                colored_frame += Fore.RED + "." + Style.RESET_ALL
            elif char == "_":
                colored_frame += Fore.GREEN + "_" + Style.RESET_ALL
            elif char == "|":
                colored_frame += Fore.YELLOW + "|" + Style.RESET_ALL
            elif char == "\\" or char == "/":
                colored_frame += Fore.BLUE + char + Style.RESET_ALL
            elif char == "(" or char == ")" or char == "O":
                colored_frame += Fore.MAGENTA + char + Style.RESET_ALL
            elif char == " ":
                colored_frame += " "
        print(colored_frame)
        time.sleep(0.2)


#Loading screen 
def show_loading_screen(engine):
    print("Welcome to the Quiz Game!")
    speak(engine, "Welcome to the Quiz Game!")
    print("Initializing...")
    speak(engine, "Initializing...")
    winsound.PlaySound('notification.wav', winsound.SND_ALIAS)
    for _ in range(10):
        time.sleep(0.5)  # Simulate loading delay
        print(".", end='', flush=True)  # Print loading indicator
    print("\nInitialization complete!\n")
    speak(engine, "Initialization complete!")

def read_instructions(engine):
    print("\nInstructions:")
    print(Instructions)
    speak(engine, "Here are the instructions for the game:")
    speak(engine, Instructions)
    while True:
        confirm = input("Do you want to continue reading the instructions? (yes/no): ").lower()
        if confirm == 'yes':
            continue
        elif confirm == 'no':
            speak(engine, "Okay, let's move on to the game.")
            break
        else:
            speak(engine, "Invalid input. Please enter 'yes' or 'no'.")

# User options
def user_options():
    play_sound()
    engine = init_text_to_speech()
    show_loading_screen(engine)
    character_user()
    while True:
        print(Fore.BLUE + "\nWhat do you want to do?")
        speak(engine, "What do you want to do?")
        print(Fore.YELLOW+ "1. Leaderboard - Be one of the top three winners!")
        speak(engine, "Option one: Leaderboard - Be one of the top three winners!")
        print(Fore.GREEN+ "2. Check your current winnings")
        speak(engine, "Option two: Check your current winnings")
        print(Fore.YELLOW+ "3. Play the game! Let's go!")
        speak(engine, "Option three: Play the game! Let's go!")
        print(Fore.RED+ "4. Exit")
        speak(engine, "Option four: Exit.")
        choice = input("Enter your choice (1/2/3/4): ")
        if choice == '1':
            show_users()
        elif choice == '2':
            user = input("Enter your Name: ").title()
            print(f'Your total amount is {users.get(user, 0)}')
            speak(engine, f'Your total amount is {users.get(user, 0)}')
        elif choice == '3':
            print("\nInstructions:")
            print(Instructions)
            speak(engine, "Instructions. " + Instructions)
            confirm = input("Are you ready to play? (yes/no): ").lower()
            if confirm == 'yes':
                user = input("Enter your Name: ").title()
                if user not in users:
                    add_user(user)
                else:
                    print("Welcome back, {}!".format(user))
                    users[user] = 0  # Resetting the amount to zero if the user already exists
                play_game(user)
            else:
                print("Thanks for Coming!")
                speak(engine, "Thanks for Coming!")
        elif choice == '4':
            print(Fore.BLUE + "Exiting the game. Goodbye!")
            speak(engine, "Exiting the game. Goodbye!")
            exit()
        else:
            print(Fore.BLUE +"Invalid choice. Please enter 1, 2, 3, or 4.")
            speak(engine, "Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    engine = init_text_to_speech()
    user_options(engine)
