import random

with open("american_words.txt", "r") as american_words:
    wrds = american_words.readlines()
words = [s.rstrip("\n") for s in wrds]
choices = {"exit", "play", "results"}
word = random.choice(words)
blank_word = "-" * len(word)
alphabet = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z'}

def hangman(blank_word):
    attempts = 8
    guesses = set()
    while attempts >= 0:
        guess = str(input(f'\n{blank_word}\ninput a letter:'))
        if len(guess) != 1:
            print("Please, input a single letter.")
        elif guess not in alphabet:
            print("Please, enter a lowercase letter from the english alphabet.")
        elif guess in guesses:
            print("You've already guessed this letter.")
        elif guess in word:
            positions = [i for i, letter in enumerate(word) if letter == guess]
            for j in positions:
                blank_word = blank_word[:j] + guess + blank_word[j+1:]
            print(f'\n# {attempts} attempts')
            guesses.add(guess)
            if blank_word == word:
                print(f'\nYou guessed the word {word}!\nYou survived!\n')
                return 'w'
        elif attempts == 0:
            print(f'\nYou lost!\nThe word was {word}')
            return 'l'
        else:
            attempts -= 1
            if attempts == 0:
                print(f'\nYou lost!\nThe word was {word}')
                return 'l'
            print(f"\nThat letter doesn't appear in the word. # {attempts} attempts")
            guesses.add(guess)


wins = 0
losses = 0
game_setting = ""
while game_setting != "exit":
    print('H A N G M A N # 8 Attempts')
    print('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    game_setting = str(input())
    if game_setting not in choices:
        print("Please choose one of the three options.")
    if game_setting == "results":
        print(f'You won: {wins} times.\nYou lost: {losses} times.')
    if game_setting == "play":
        score = hangman(blank_word)
        if score == 'l':
            losses += 1
        if score == 'w':
            wins += 1

