from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
scratch_cards = input_file.readlines()


def parse_inputs(lines):
    card_quantities = [1] * len(lines)
    for i, line in enumerate(lines):
        line = line.strip()
        data = line.split(': ')[1]
        my_numbers, winning_numbers = data.split(' | ')
        my_numbers = list(
            filter(lambda n: n.isnumeric(), my_numbers.split(' ')))
        winning_numbers = list(
            filter(lambda n: n.isnumeric(), winning_numbers.split(' ')))

        matches = 0
        for n in my_numbers:
            if n in winning_numbers:
                matches += 1

        for j in range(matches):
            if j + 1 < len(card_quantities):
                card_quantities[i + j + 1] += card_quantities[i]

    return card_quantities


def solution():
    card_quantities = parse_inputs(scratch_cards)
    return sum(card_quantities)


print(solution())
