"""Song Quiz - login, quiz and leaderboard.

Originally written for my GCSE Computer Science controlled assessment,
then tidied up and bug-fixed. Songs live in Quiz.txt (song:artist),
players in users.txt (name:username:password) and results in
Score.txt (name:score:percent).
"""
import random

USERS_FILE = "users.txt"
QUIZ_FILE = "Quiz.txt"
SCORE_FILE = "Score.txt"
MAX_ROUNDS = 10


def read_lines(filename):
    """Return the non-empty lines of a file, or [] if it doesn't exist yet."""
    try:
        with open(filename) as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []


def get_choice(prompt, allowed):
    """Keep asking until the answer is one of the allowed options."""
    while True:
        answer = input(prompt).strip()
        if answer in allowed:
            return answer
        print("Invalid choice, try again.")


def login_menu():
    while True:
        print("\n1 for New user, 2 for Existing user, -1 to exit")
        choice = get_choice(":", ["1", "2", "-1"])
        if choice == "1":
            new_login()
        elif choice == "2":
            name = login()
            if name:
                main_menu(name)
        else:
            print("Goodbye!")
            break


def main_menu(name):
    while True:
        print(f"\nCurrent user: {name}")
        print("1 for Quiz, 2 for Leaderboard, -1 to logout")
        choice = get_choice(":", ["1", "2", "-1"])
        if choice == "1":
            quiz(name)
        elif choice == "2":
            leaderboard()
        else:
            print("Logged out")
            break


def new_login():
    name = input("What's your name: ").strip()
    while not name.isalpha():
        print("Invalid - letters only")
        name = input("What's your name: ").strip()

    age = input("What's your age: ").strip()
    while not (age.isdigit() and 1 <= int(age) <= 120):
        print("Invalid - enter a number from 1 to 120")
        age = input("What's your age: ").strip()

    user = name[:4] + age
    taken = [line.split(":", 2)[1] for line in read_lines(USERS_FILE)]
    if user in taken:
        print(f"The username {user} is already taken.")
        return
    print(f"Your username is {user}")

    password = input("Make a password (8+ characters): ")
    while len(password) < 8:
        print("Invalid - too short")
        password = input("Make a password (8+ characters): ")

    with open(USERS_FILE, "a") as login_file:
        login_file.write(f"\n{name}:{user}:{password}")
    print("Account created - you can now log in.")


def login():
    """Return the player's name if they log in, or None after 3 failed tries."""
    users = read_lines(USERS_FILE)  # read once into a list so retries work
    for _ in range(3):
        username = input("Username: ").strip()
        password = input("Password: ")
        for line in users:
            name, user, stored_password = line.split(":", 2)
            if username == user and password == stored_password:
                print(f"Welcome {name}")
                return name
        print("Wrong username or password.")
    print("Too many attempts.")
    return None


def hint(title):
    """First letter, then an underscore for every other letter or number."""
    shown = [title[0]]
    for char in title[1:]:
        shown.append("_" if char.isalnum() else char)
    return " ".join(shown)


def quiz(name):
    songs = []
    for line in read_lines(QUIZ_FILE):
        song_name, artist_name = line.rsplit(":", 1)
        songs.append((song_name, artist_name))
    if not songs:
        print("No songs found in Quiz.txt")
        return

    random.shuffle(songs)
    songs = songs[:MAX_ROUNDS]
    score = 0

    for round_number, (song_name, artist_name) in enumerate(songs, 1):
        print(f"\nRound {round_number}")
        print(f"{hint(song_name)} by {artist_name}")
        for attempt in range(2):  # two guesses
            guess = input("What is your guess? ").strip()
            if guess.lower() == song_name.lower():
                points = 3 if attempt == 0 else 1
                score += points
                print(f"Correct! +{points}")
                break
            print("Wrong")
        else:  # only runs if neither guess was right
            print(f"The answer was {song_name}")

    percent = round(score / (len(songs) * 3) * 100)
    print(f"\nWell done {name}, you scored {score} ({percent}%)")
    with open(SCORE_FILE, "a") as score_file:
        score_file.write(f"\n{name}:{score}:{percent}")
    leaderboard()


def leaderboard():
    scores = []
    for line in read_lines(SCORE_FILE):
        name, score, percent = line.split(":")
        scores.append((name, int(score), percent))
    print("\n--- Leaderboard (top 10) ---")
    if not scores:
        print("No scores yet.")
        return
    scores.sort(key=lambda entry: entry[1], reverse=True)  # highest first
    for place, (name, score, percent) in enumerate(scores[:10], 1):
        print(f"{place}. {name} - {score} points ({percent}%)")


if __name__ == "__main__":
    login_menu()
