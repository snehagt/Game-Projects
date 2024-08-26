import json

def save_users_data(users):
    with open('users_data.json', 'w') as file:
        json.dump(users, file)

def load_users_data():
    try:
        with open('users_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def add_user(user):
    if user not in users:
        users[user] = 0
        save_users_data(users)

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

def show_users():
    top_users = sorted(users.items(), key=lambda x: x[1], reverse=True)
    print("Rank | Player   | Amount Won")
    print("-" * 30)
    for rank, (user, amount) in enumerate(top_users[:3], start=1):
        print(f"{rank:<4} | {user:<8} | {amount:>5} Rs only/-")

# Load users data
users = load_users_data()
