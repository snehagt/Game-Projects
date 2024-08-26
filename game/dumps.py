# def play_game(user):
#     for i, (question, choices) in enumerate(questions.items(), start=1):
#         print(f'{i}. {question}:')
#         for letter, choice in zip(string.ascii_uppercase, choices):
#             print(f'   {letter}. {choice}')
#         answer = get_answer()
#         amount = calculate_user_amount(i, question, answer)
#         users[user] += amount
#         if amount > 0:
#             print(f"Correct answer! You win {amount} Rs.")
#         else:
#             print("Wrong answer. You lose!")
#             break
#         save_users_data(users)
#         check_user_amount(user)
#         if users[user] == 0:
#             print("Sorry, your total amount is 0. You lose!")
#             exit()

# def amount_calculation(user, ques_number, answer, questions):
#     correct_answer = questions[ques_number][0][0]
#     if answer == correct_answer:
#         if 1 <= ques_number <= 5:
#             users[user] += 5000
#         elif 6 <= ques_number <= 10:
#             users[user] += 15000
#         print(f"Correct answer! You win {users[user]} Rs.")
#     else:
#         if 1 <= ques_number <= 5:
#             users[user] = 0
#         elif 6 <= ques_number <= 10:
#             users[user] = 25000
#         print("Wrong answer. You lose!")
#     save_users_data(users)


import random
import string
from instructions import Instructions
from questions import questions
from users import users, add_user, check_user_amount, show_users
from users import save_users_data

def display_questions(questions, ques_number):
    shuffled_questions = list(questions.keys())
    random.shuffle(shuffled_questions)

    shuffled_question = shuffled_questions[0]
    choices = questions[shuffled_question]
    random.shuffle(choices)

    print(f'{ques_number}. {shuffled_question}:')
    for ques_number, choice in zip(string.ascii_uppercase, choices):
        print(f'   {ques_number}. {choice}')

def get_answer():
    while True:
        ans = input("Enter your choice: ").upper()
        if ans in string.ascii_uppercase:
            return ans
        else:
            print("Invalid choice. Please enter a valid option.")

def calculate_user_amount(user, question_number, question, answer):
    question_number = int(question_number)  # Convert question_number to an integer
    correct_answer = questions[question][0]
    if answer.upper() == string.ascii_uppercase[questions[question].index(correct_answer)]:
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
        shuffled_questions = list(questions.keys())
        random.shuffle(shuffled_questions)
        shuffled_question = shuffled_questions[0]

        display_questions({shuffled_question: questions[shuffled_question]}, i)
        answer = get_answer()

        # Lifeline 50-50
        if answer == 'L':  # Using 'L' as the lifeline activation key
            choices = lifeline_50_50(questions[shuffled_question], 'A')  # Assuming correct answer is always 'A'
            print("50-50 Lifeline used. Choices left:")
            for choice in choices:
                print(choice)
            answer = get_answer()

        amount = calculate_user_amount(user, i, shuffled_question, answer)

        if amount > 0:
            print(f"Correct answer! You win {amount} Rs.")
        else:
            print(f"Wrong answer. You lose! Your total amount is {users[user]} Rs.")
            exit()

        save_users_data(users)
        calculate_user_amount(user, i, shuffled_question, answer)

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


# # Lifeline Double Dip
# if answer == 'DD':  # Using 'DD' as the lifeline activation key for Double Dip
#     if lifeline_double_dip(questions[shuffled_question], 'A'):  # Assuming correct answer is always 'A'
#         amount = calculate_user_amount(user, i, shuffled_question, answer)  # Calculate amount based on lifeline usage
#         print(f"Correct answer! You win {amount} Rs.")
#         continue
#     else:
#         print("Wrong answer. You lose! Your total amount is Rs. 0.")
#         exit()
## This is the KBC CODE
# import random
# import string
# from instructions import Instructions
# from questions import questions
# from users import users, add_user, show_users
# from users import save_users_data

# def display_questions(questions, ques_number):
#     shuffled_questions = list(questions.keys())
#     random.shuffle(shuffled_questions)

#     shuffled_question = shuffled_questions[0]
#     choices = questions[shuffled_question]
#     random.shuffle(choices)

#     print(f'{ques_number}. {shuffled_question}:')
#     for ques_number, choice in zip(string.ascii_uppercase, choices):
#         print(f'   {ques_number}. {choice}')

#     return shuffled_question

# def get_answer():
#     while True:
#         ans = input("Enter your choice: ").upper()
#         if ans in string.ascii_uppercase:
#             return ans
#         else:
#             print("Invalid choice. Please enter a valid option.")

# def calculate_user_amount(user, question_number, question, answer):
#     question_number = int(question_number)  # Convert question_number to an integer
#     correct_answer = questions[question][0]
#     if answer.upper() == string.ascii_uppercase[questions[question].index(correct_answer)]:
#         if 1 <= question_number <= 5:
#             amount = 5000
#         elif 6 <= question_number <= 10:
#             amount = 15000
#     else:
#         if 1 <= question_number <= 5:
#             amount = 0
#         elif 6 <= question_number <= 10:
#             amount = 25000
#     users[user] += amount
#     save_users_data(users)
#     return amount

# def lifeline_50_50(choices, correct_answer):
#     incorrect_choices = [choice for choice in choices if choice != correct_answer]
#     choices_to_remove = random.sample(incorrect_choices, 2)
#     for choice in choices_to_remove:
#         choices.remove(choice)
#     return choices

# def play_game(user):
#     for i in range(1, len(questions) + 1):

#         shuffled_question = display_questions(questions, i)
#         answer = get_answer()

#         # Lifeline 50-50
#         if answer == 'L':  # Using 'L' as the lifeline activation key
#             choices = lifeline_50_50(questions[shuffled_question], questions[shuffled_question][0])  # Assuming correct answer is always 'A'
#             print("50-50 Lifeline used. Choices left:")
#             for choice in choices:
#                 print(choice)
#             answer = get_answer()

#         amount = calculate_user_amount(user, i, shuffled_question, answer)

#         if amount > 0:
#             print(f"Correct answer! You win {amount} Rs.")
#         else:
#             print(f"Wrong answer. You lose! Your total amount is {users[user]} Rs.")
#             exit()

#         save_users_data(users)
#         calculate_user_amount(user, i, shuffled_question, answer)

#         if users[user] == 0:
#             print("Sorry, your total amount is 0. You lose!")
#             exit()

# def user_options():
#     while True:
#         print("\nOptions:")
#         print("1. Players won - list 3 top players")
#         print("2. Your current amount")
#         print("3. Play the game")
#         print("4. Exit")
#         choice = input("Enter your choice (1/2/3/4): ")

#         if choice == '1':
#             show_users()
#         elif choice == '2':
#             user = input("Enter your Name: ").title()
#             print(f'Your total amount is {users[user]}')
#         elif choice == '3':
#             print("\nInstructions:")
#             print(Instructions)
#             confirm = input("Are you ready to play? (yes/no): ").lower()
#             if confirm == 'yes':
#                 user = input("Enter your Name: ").title()
#                 if user not in users:
#                     add_user(user)
#                 else:
#                     print("Welcome back, {}!".format(user))
#                     users[user] = 0  # Resetting the amount to zero if the user already exists
#                 play_game(user)
#             else:
#                 print("Thanks for Coming!")
#         elif choice == '4':
#             print("Exiting the game. Goodbye!")
#             exit()
#         else:
#             print("Invalid choice. Please enter 1, 2, 3, or 4.")

# if __name__ == "__main__":
#     user_options()


def check_user_amount(user):
    user_lower = user.lower()  
    try:
        amount = users[user_lower]
        print(f'Your total amount during your game play is {amount}. Thanks for Playing.')
    except KeyError:
        print("You are not currently registered in the game.")
        add_user()
        amount = users[user_lower]
        print(f'Your total amount during your game play is {amount}. Thanks for Playing.')
