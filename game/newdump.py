import random
import string
from instructions import Instructions
from questions import questions
from users import users, add_user, show_users
from users import save_users_data

def display_questions(questions, ques_number):
    shuffled_questions = list(questions.keys())
    random.shuffle(shuffled_questions)

    shuffled_question = shuffled_questions[0]
    choices = questions[shuffled_question]
    correct_answer=choices[0]
    random.shuffle(choices)

    print(f'{ques_number}. {shuffled_question}:')
    for ques_number, choice in zip(string.ascii_uppercase, choices):
        print(f'   {ques_number}. {choice}')

    return shuffled_question, choices, correct_answer

def get_answer():
    while True:
        ans = input("Enter your choice: ").upper()
        if ans in string.ascii_uppercase:
            return ans
        else:
            print("Invalid choice. Please enter a valid option.")

def calculate_user_amount(user, question_number, answer, shuffled_choices,correct_answer):

    question_number = int(question_number)
    if shuffled_choices[ord(answer)-65]==correct_answer:
        if 1 <= question_number <= 5:
            amount = 5000
        elif 6 <= question_number <= 10:
            amount = 15000
    else:
        if 1 <= question_number <= 5:
            amount = 0
        elif 6 <= question_number <= 10:
            amount = 25000
    users[user] += amount
    save_users_data(users)
    return amount

def lifeline_50_50(choices, correct_answer):
    incorrect_choices = [choice for choice in choices if choice != correct_answer]
    choices_to_remove = random.sample(incorrect_choices, 2)
    for choice in choices_to_remove:
        choices.remove(choice)
    return choices

def play_game(user):
    for i in range(1, len(questions) + 1):

        shuffled_question, shuffled_choices,correct_answer = display_questions(questions, i)
        answer = get_answer()

        # Lifeline 50-50
        if answer == 'L':  # Using 'L' as the lifeline activation key
            choices = lifeline_50_50(questions[shuffled_question], questions[shuffled_question][0])  # Assuming correct answer is always 'A'
            print("50-50 Lifeline used. Choices left:")
            for choice in choices:
                print(choice)
            answer = get_answer()

        amount = calculate_user_amount(user, i, answer, shuffled_choices,correct_answer)

        if amount > 0:
            print(f"Correct answer! You win {amount} Rs.")
        else:
            print(f"Wrong answer. You lose! Your total amount is {users[user]} Rs.")
            exit()

        save_users_data(users)
        calculate_user_amount(user, i, answer, shuffled_choices,correct_answer)

        if users[user] == 0:
            print("Sorry, your total amount is 0. You lose!")
            exit()

def user_options():
    while True:
        print("\nOptions:")
        print("1. Players won - list 3 top players")
        print("2. Your current amount")
        print("3. Play the game")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            show_users()
        elif choice == '2':
            user = input("Enter your Name: ").title()
            print(f'Your total amount is {users[user]}')
        elif choice == '3':
            print("\nInstructions:")
            print(Instructions)
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
        elif choice == '4':
            print("Exiting the game. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    user_options()


def game(user_choice, computer_choice):
    while True:
        if user_choice == computer_choice:
            print("Game ties! No one wins. Try again")
        elif ((user_choice == 1 and computer_choice == 2) or \
                (user_choice == 2 and computer_choice == 3) or \
                user_choice == 3 and computer_choice == 1):
                print('You Lose!')
        elif user_choice == 1 and computer_choice == 3:
            print('You win!')
        elif user_choice == 2 and computer_choice == 1:
            print('You win!')
        elif user_choice == 3 and computer_choice == 2:
            print('You win!')