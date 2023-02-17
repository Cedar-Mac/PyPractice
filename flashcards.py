import shutil
import jsonpickle
import random
import argparse
from io import StringIO

memory_file = StringIO()

parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')
args = parser.parse_args()


class Flashcards(object):
    cards = {}
    number_of_card = len(cards)

    def __init__(self):
        memory_file.read()
        Flashcards.number_of_card += 1
        self.card_number = Flashcards.number_of_card
        self.mistakes_counter = 0
        print(f'The term for card #{self.card_number}: ')
        memory_file.write(f'The term for card #{self.card_number}: ')
        while True:
            self.term = str(input())
            memory_file.write(self.term)
            if self.term in [card.term for card in Flashcards.cards.values()]:
                print(f'The term "{self.term}" already exists. Try again:')
                memory_file.write(f'The term "{self.term}" already exists. Try again:')
            else:
                break
        print(f'The definition for card #{self.card_number}: ')
        memory_file.write(f'The definition for card #{self.card_number}: ')
        while True:
            self.definition = str(input())
            memory_file.write(self.definition)
            if self.definition in [card.definition for card in Flashcards.cards.values()]:
                print(f'The definition "{self.definition}" already exists. Try again:')
                memory_file.write(f'The definition "{self.definition}" already exists. Try again:')
            else:
                break

    def test_user(self):
        memory_file.read()
        print(f'Print the definition of "{self.term}" ')
        memory_file.write(f'Print the definition of "{self.term}" ')
        guess = str(input())
        memory_file.write(guess)
        if guess == self.definition:
            print('Correct!')
            memory_file.write('Correct!')
        elif guess in [card.definition for card in Flashcards.cards.values()]:
            print(f'Wrong. The right answer is "{self.definition}", but your definition is correct for '
                  f'"{[card.term for card in Flashcards.cards.values() if card.definition == guess][0]}".')
            memory_file.write(f'Wrong. The right answer is "{self.definition}", but your definition is correct for '
                              f'"{[card.term for card in Flashcards.cards.values() if card.definition == guess][0]}".')
            self.mistakes_counter += 1
        elif guess != self.definition:
            print(f'Wrong. The right answer is {self.definition}')
            memory_file.write(f'Wrong. The right answer is {self.definition}')
            self.mistakes_counter += 1


def add_card():
    memory_file.read()
    Flashcards.cards[f'card #{Flashcards.number_of_card}'] = Flashcards()
    print(f'The pair ("{Flashcards.cards.get(f"card #{Flashcards.number_of_card}").term}":\
    "{Flashcards.cards.get(f"card #{Flashcards.number_of_card}").definition}") has been added.')
    memory_file.write(f'The pair ("{Flashcards.cards.get(f"card #{Flashcards.number_of_card}").term}":\
    "{Flashcards.cards.get(f"card #{Flashcards.number_of_card}").definition}") has been added.')
    return Flashcards.cards


def remove_card():
    memory_file.read()
    print('Which card?')
    memory_file.write('Which card?')
    del_card = str(input())
    memory_file.write(del_card)
    try:
        Flashcards.cards.pop([card for card, card_stat in Flashcards.cards.items() if card_stat.term == del_card][0])
        Flashcards.number_of_card -= 1
        print('The card has been removed.')
        memory_file.write('The card has been removed.')
    except IndexError:
        print(f'Can\'t remove "{del_card}": there is no such card.')
        memory_file.write(f'Can\'t remove "{del_card}": there is no such card.')


def import_cards():
    memory_file.read()
    print('File name:')
    memory_file.write('File name:')
    import_name = str(input()).rstrip('.txt')
    memory_file.write(import_name)
    try:
        with open(f'{import_name}.txt', 'r') as file:
            new_cards = jsonpickle.decode(file.read(), classes=Flashcards)
            Flashcards.cards.update(new_cards)
            print(f'{len(new_cards) + 1} cards have been loaded.')
            memory_file.write(f'{len(new_cards) + 1} cards have been loaded.')
        Flashcards.number_of_card = len(Flashcards.cards.values())
    except FileNotFoundError:
        print('File not found.')
        memory_file.write('File not found.')


def export_cards():
    memory_file.read()
    print('File name:')
    memory_file.write('File name:')
    export_name = str(input()).rstrip('.txt ')
    memory_file.write(export_name)
    try:
        with open(f'{export_name}.txt', 'w') as file:
            file.write(jsonpickle.encode(Flashcards.cards))
        print(f'{Flashcards.number_of_card} cards have been saved.')
        memory_file.write(f'{Flashcards.number_of_card} cards have been saved.')
    except ValueError:
        print("Couldn't write file")
        memory_file.write("Couldn't write file")


def export_log():
    memory_file.read()
    print('File name:')
    memory_file.write('File name:')
    export_name = str(input()).rstrip('.txt ')
    memory_file.write(export_name)
    try:
        with open(f'{export_name}.txt', 'w') as log:
            memory_file.seek(0)
            shutil.copyfileobj(memory_file, log, -1)
        print('The log has been saved.')
        memory_file.write('The log has been saved.')
    except ValueError:
        print("Couldn't write file")
        memory_file.write("Couldn't write file")


def review_terms():
    memory_file.read()
    print('How many times to ask?')
    memory_file.write('How many times to ask?')
    number_to_review = int(input())
    memory_file.write(str(number_to_review))
    try:
        x = 0
        while x < number_to_review:
            random.choice(list(Flashcards.cards.values())).test_user()
            x += 1
    except IndexError:
        print('No cards to review.')
        memory_file.write('No cards to review.')


def check_stats():
    memory_file.read()
    most_misses = 1
    for card in Flashcards.cards.values():
        if card.mistakes_counter > most_misses:
            most_misses = card.mistakes_counter

    hardest_cards = {stat.term: stat.mistakes_counter for stat in Flashcards.cards.values() if
                     stat.mistakes_counter == most_misses}
    formatter = '{}, ' * len(hardest_cards)
    if len(hardest_cards) == 0:
        print('There are no cards with errors.')
        memory_file.write('There are no cards with errors.')
    if len(hardest_cards) == 1:
        print('The hardest card is "{}". You have {} errors answering it'.format(*hardest_cards, most_misses))
        memory_file.write('The hardest card is "{}". You have {} errors answering it'.format(*hardest_cards, most_misses))
    if len(hardest_cards) > 1:
        print('The hardest cards are {}, {}'.format(*hardest_cards))
        memory_file.write('The hardest cards are {}, {}'.format(*hardest_cards))


def reset_stats():
    memory_file.read()
    for card in Flashcards.cards.values():
        card.mistakes_counter = 0
    print('Card statistics have been reset')
    memory_file.write('Card statistics have been reset')


def pick_action():
    memory_file.read()
    while True:
        print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        memory_file.write('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        choice = str(input())
        memory_file.write(choice)
        if choice == 'add':
            add_card()
        if choice == 'remove':
            remove_card()
        if choice == 'import':
            import_cards()
        if choice == 'export':
            export_cards()
        if choice == 'ask':
            review_terms()
        if choice == 'log':
            export_log()
        if choice == 'hardest card':
            check_stats()
        if choice == 'reset stats':
            reset_stats()
        if choice == 'exit':
            print('Bye bye!')
            memory_file.write('Bye bye!')
            if args.export_to is not None:
                with open(f'{args.export_to}', 'w') as file:
                    file.write(jsonpickle.encode(Flashcards.cards))
                print(f'{Flashcards.number_of_card} cards have been saved.')
                memory_file.write(f'{Flashcards.number_of_card} cards have been saved.')
            exit()


if args.import_from is not None:
    with open(f'{args.import_from}', 'r') as file:
        new_cards = jsonpickle.decode(file.read(), classes=Flashcards)
    Flashcards.cards.update(new_cards)
    Flashcards.number_of_card = len(Flashcards.cards.values())
    print(f'{len(new_cards)} cards have been loaded.')
    memory_file.write(f'{len(new_cards) + 1} cards have been loaded.')

pick_action()
