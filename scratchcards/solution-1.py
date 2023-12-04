from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
scratch_cards = input_file.readlines()

def parse_inputs(lines):
    monies = 0
    for line in lines:
        line = line.strip()
        data = line.split(': ')[1]
        my_numbers, winning_numbers = data.split(' | ')
        my_numbers = list(filter(lambda n: n.isnumeric(), my_numbers.split(' ')))
        winning_numbers = list(filter(lambda n: n.isnumeric(), winning_numbers.split(' ')))
        
        matches = 0
        for n in my_numbers:
            if n in winning_numbers:
                matches += 1
        
        if matches > 0:
            monies += 2**(matches - 1)
    
    return monies
    


def solution():
    total_earned = parse_inputs(scratch_cards)
    return total_earned


print(solution())
