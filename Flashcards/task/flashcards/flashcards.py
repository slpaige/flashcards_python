import json
import random
import sys
import argparse


class FlashCard:

    global cards

    term = ""
    definition = ""
    mistakes = 0

    def __init__(self, term, definition, mistakes=0):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes

    def __repr__(self):
        return f'The pair ("{self.term}":"{self.definition}") has been added.'


def logit(message):
    global log
    log.append(message)
    print(message)


def check_dup_term(term):
    global cards

    if len(cards) == 0:
        return False

    for search in cards:
        if term == search.term:
            logit(f'The card "{term}" already exists. Try again:')
            return True
    return False


def check_dup_def(definition):
    global cards

    if len(cards) == 0:
        return False

    for search in cards:
        if definition == search.definition:
            logit(f'The definition "{definition}" already exists. Try again:')
            return True
    return False


def add_card():
    logit("The card:")
    while True:
        the_term = input()
        logit(the_term)
        if not check_dup_term(the_term):
            break

    logit("The definition of the card:")
    while True:
        the_def = input()
        logit(the_def)
        if not check_dup_def(the_def):
            break

    new_card = FlashCard(the_term, the_def)
    cards.append(new_card)
    logit(new_card.__repr__())


def remove_card():
    global cards

    logit("Which card?")
    card_to_remove = input()
    logit(card_to_remove)

    idx_to_remove = -1

    for idx, search in enumerate(cards):
        if card_to_remove == search.term:
            idx_to_remove = idx

    if idx_to_remove >= 0:
        cards.pop(idx_to_remove)
        logit("The card has been removed.")
    else:
        logit(f'Can\'t remove "{card_to_remove}": there is no such card.')


def find(term):
    global cards
    if len(cards) == 0:
        return -1

    for idx, search in enumerate(cards):
        if term == search.term:
            return idx
    return -1


def import_cards(import_path=""):
    global cards

    if import_path == "":
        logit("File name:")
        file_name = input()
    else:
        file_name = import_path

    logit(file_name)

    try:
        with open(f"{file_name}", "r") as input_file:
            imp_cards = json.load(input_file)

        for key, value in imp_cards.items():
            if key != "":
                search_index = find(key)
                split_def, split_mistake = value.split("|")
                if search_index >= 0:
                    cards[search_index].definition = split_def
                    cards[search_index].mistakes = int(split_mistake)
                else:
                    cards.append(FlashCard(key, split_def, int(split_mistake)))

        logit(f"{len(imp_cards)} cards have been loaded.")

    except FileNotFoundError:
        print("File not found.")


def export_cards(export_path=""):
    global cards

    if export_path == "":
        logit("File name:")
        file_name = input()
    else:
        file_name = export_path

    logit(file_name)

    exp_cards = {}
    for exp_card in cards:
        exp_cards[exp_card.term] = f"{exp_card.definition}|{exp_card.mistakes}"

    with open(f"{file_name}", "w") as outfile:
        outfile.write(json.dumps(exp_cards))

    logit(f"{len(cards)} cards have been saved.")


def ask():
    global cards
    logit("How many times to ask?")
    num_cards = int(input())

    for guess_iteration in range(1, num_cards + 1):
        guess_card = random.choice(cards)
        logit(f'Print the definition of "{guess_card.term}":')
        the_guess = input()
        logit(the_guess)

        if the_guess != guess_card.definition:
            was_found = False
            for search_card in cards:
                if search_card.definition == the_guess:
                    logit(f'Wrong. The right answer is "{guess_card.definition}", but your definition is correct for '
                          f'"{search_card.term}".')
                    was_found = True

            if not was_found:
                logit(f'Wrong. The right answer is "{guess_card.definition}"')

            guess_card.mistakes += 1
        else:
            logit("Correct!")


def hardest_card():
    global cards
    hard_cards = []
    max_errors = 0

    for card in cards:
        if card.mistakes == max_errors and card.mistakes > 0:
            hard_cards.append(card.term)
            max_errors = card.mistakes
            print(card.mistakes)
        elif card.mistakes > max_errors:
            hard_cards = [card.term]
            max_errors = card.mistakes
            print(card.mistakes)

    card_cards = "card" if len(hard_cards) == 1 else "cards"
    it_them = "it" if len(hard_cards) == 1 else "them"
    is_are = "is" if len(hard_cards) == 1 else "are"

    if len(hard_cards) > 0:
        logit(f"The hardest {card_cards} {is_are} \"{', '.join(hard_cards)}\". You have {max_errors} errors answering "
              f"{it_them}.")
    else:
        logit("There are no cards with errors.")


def reset_stats():
    for card in cards:
        card.mistakes = 0

    logit("Card statistics have been reset.")


def log_it():
    global log
    logit("File name:")
    file_name = input()
    logit(file_name)

    with open(file_name, "w") as file:
        file.write('\n'.join(log))

    logit("The log has been saved.")


cards = []
log = []

parser = argparse.ArgumentParser()
parser.add_argument("--import_from", default="", type=str)
parser.add_argument("--export_to", default="", type=str)

passed_args = parser.parse_args()
import_from = passed_args.import_from
export_to = passed_args.export_to

if import_from != "":
    import_cards(import_from)

while True:
    logit("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
    action = input()
    logit(action)

    match action:
        case "add":
            add_card()
        case "remove":
            remove_card()
        case "import":
            import_cards()
        case "export":
            export_cards()
        case "ask":
            ask()
        case "log":
            log_it()
        case "hardest card":
            hardest_card()
        case "reset stats":
            reset_stats()
        case "exit":
            print("Bye bye!")
            if export_to != "":
                export_cards(export_to)
            break
