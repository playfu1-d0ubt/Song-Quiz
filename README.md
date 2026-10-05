# Song Quiz

A console game written in Python. Players log in, guess songs from the first letter of the title and the artist's name, and compete on a leaderboard.

I first wrote it for my GCSE Computer Science controlled assessment, then came back later to fix bugs and tidy it up.

## Features

- Login system with new accounts (username = first 4 letters of your name + your age)
- Songs and artists loaded from a text file you can edit
- Shows the first letter of the title, with blanks for the rest
- Two guesses per song: 3 points for a first-time answer, 1 point for a second
- Total score and percentage at the end of the game
- Scores saved to a file, with a top 10 leaderboard

## How to run

You need Python 3.

```
python3 song_quiz.py
```

| File | What it does |
| --- | --- |
| `song_quiz.py` | The game |
| `Quiz.txt` | One song per line as `song:artist`. Swap in your own |
| `users.txt` | Created automatically when the first account is made (`name:username:password`) |
| `Score.txt` | Created automatically after the first game (`name:score:percent`) |

## How it works

The program is split into small functions: `login_menu`, `main_menu`, `new_login`, `login`, `quiz`, `leaderboard` and a few helpers. I planned it in pseudocode first, then built and tested it one function at a time.

## Testing

I planned tests for each input using normal, boundary and erroneous data:

| What I tested | Normal | Boundary | Erroneous |
| --- | --- | --- | --- |
| Username | Bon15 | james7 | karen |
| Password | Password | passwor | 4.80 |
| Menu choice | 1, -1 | -2, 3 | A, 7.4 |
| Name | Bon | james | 7 |
| Age | 12 | - | James |
| Guess | Half-life | - | 12 |

Bugs I found and fixed along the way:

- A missing `int()` around menu input, so choices never matched
- An attribute error caused by a mistake with `strip`
- Pressing Enter twice kept repeating the last username
- Login only worked for a few lines of the user file, and retries failed

## What I'd do next

- Passwords are stored as plain text. That is fine for learning but not for a real app, so the next step is hashing them
- Add more song categories or difficulty levels
- Let players pick how many rounds to play
