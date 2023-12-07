import functools
from pathlib import Path
current_working_directory = Path.cwd()
input_file = open(str(current_working_directory) + '/input.txt', 'r')
card_bets = input_file.readlines()

alpha_order = ['A', 'K', 'Q', 'J', 'T']


def compare(card_one, card_two):
    # is card_one > card_two, None if equal
    if card_one == card_two:
        return None
    elif card_one.isnumeric() and card_two.isnumeric():
        return int(card_one) > int(card_two)
    elif card_one.isalpha() and card_two.isalpha():
        return alpha_order.index(card_one) < alpha_order.index(card_two)
    else:
        return card_one.isalpha()


def get_type(hand):
    tokenized_hand = list(hand)
    tokenized_hand_set = set(tokenized_hand)
    if len(tokenized_hand_set) == 1:
        return 0  # 'five-of-a-kind'
    elif len(tokenized_hand_set) == 2:
        # can be either full house or four of a kind
        first_card_count = tokenized_hand.count(tokenized_hand[0])
        if first_card_count == 2 or first_card_count == 3:
            return 2  # 'full-house'
        else:
            return 1  # 'four-of-a-kind'
    elif len(tokenized_hand_set) == 3:
        # can either be two pair or three of a kind
        for card_type in list(tokenized_hand_set):
            if tokenized_hand.count(card_type) == 3:
                return 3  # 'three-of-a-kind'
        return 4  # 'two-pair'
    elif len(tokenized_hand_set) == 4:
        return 5  # 'one-pair'
    else:
        return 6  # 'high-card'


def parse_inputs(lines):
    hands = []
    bets_map = {}
    for line in lines:
        line = line.strip()
        hand, bet = line.split(' ')
        bet = int(bet)
        hands.append(hand)
        bets_map[hand] = bet

    return hands, bets_map


def custom_sort(hand_one, hand_two):
    hand_one_type = get_type(hand_one)
    hand_two_type = get_type(hand_two)
    if hand_one_type != hand_two_type:
        return 1 if hand_one_type < hand_two_type else -1
    else:
        for (card_one, card_two) in zip(hand_one, hand_two):
            result = compare(card_one, card_two)
            if result != None:
                return 1 if result else -1
        # shouldn't ever be equal
        raise Exception('impossible')


def solution():
    hands, bets_map = parse_inputs(card_bets)
    sorted_hands = sorted(hands, key=functools.cmp_to_key(custom_sort))
    total_score = 0
    for i, hand in enumerate(sorted_hands):
        total_score += ((i+1) * bets_map[hand])

    return total_score


print(solution())
