import random

cards = [
    ('move', 1), ('move', 1), ('move', 1), ('move', 1),
    ('move', 2), ('move', 2), ('move', 2), ('move', 2),
    ('move', 3), ('move', 3), ('move', 3), ('move', 3),
    ('move', 4), ('move', 4), ('move', 4), ('move', 4),
    ('move', 'again', 2), ('move', 'again', 2), ('move', 'again', 2), ('move', 'again', 2),
    ('move', 'again', 3), ('move', 'again', 3), ('move', 'again', 3),
    ('move', 'again', 4), ('move', 'again', 4),
    ('move', -1), ('move', -2), ('move', -3),
    ('move', 'again', -4), ('move', 'again', -4),
    ('aphid', 1), ('aphid', 2), ('aphid', 3), ('aphid', 3), ('aphid', 4)
]

board = [
    'start', '_', '_', ('aphid', 3), 'mantis_pass', '_', 'slide', '_', 'mantis_pass', 'mantis', '_', '_', '_',
    ('aphid', 2), '_',
    ('aphid', 5), '_', ('aphid', -2), '_', '_', ('move', -2), '_', '_', ('aphid', -1),
    '_', '_', 'ants', '_', 'lose_turn', '_', '_', '_', 'lose_turn', '_', '_', 'home'
]

ant_loop = [
    '_', ('aphid', 1), '_', ('aphid', 3), '_', ('move', -2), '_'
]


def time_for_ants(currrent_spot, movement):
    return currrent_spot < 26 <= currrent_spot + movement


def draw_random_card(random_card_list):
    card = random_card_list[0]
    if len(random_card_list) == 1:
        for num in range(35):
            random_card_list.append(num)
        random.shuffle(random_card_list)
    else:
        random_card_list.remove(card)
    return card


class Ladybug:
    def __init__(self, name):
        self.name = name
        self.aphids = 0
        self.mantis_pass = False
        self.pos = 0
        self.lose_turn = False
        self.in_ant_loop = False

    def show_inventory(self):
        print(f'Aphids: {self.aphids}')
        if self.in_ant_loop:
            print(f'Location: {self.pos}/6 (in the ant loop)')
        else:
            print(f'Location: {self.pos}/35')
            if self.pos < 10:
                print(f"Mantis pass: {'yes' if self.mantis_pass else 'no'}")

    def draw_card(self, random_card_list):
        card = cards[draw_random_card(random_card_list)]
        if card[0] == 'move':
            self.move(card[-1])
            if len(card) == 3:
                print(f'>> draw again')
                self.draw_card(random_card_list)
        elif card[0] == 'aphid':
            print(f'>> get {card[-1]} aphids')
            self.aphids += card[-1]

    def move(self, steps):
        print(f'>> move {steps} spaces')
        if self.time_to_leave_loop(steps):
            self.pos += steps + 15
            self.in_ant_loop = False
        elif self.pos + steps > 35:
            self.pos = 35
        elif self.pos + steps < 0:
            if self.in_ant_loop:
                self.pos += 26 + steps
                self.in_ant_loop = False
            self.pos = 0
        elif time_for_ants(self.pos, steps):
            self.face_the_ants(steps)
        else:
            self.pos += steps
        self.analyze_new_spot()

    def one_turn(self, random_card_list):
        print(f'\n{self.name}\'s turn!')
        if self.lose_turn:
            print(f'{self.name} lost this turn')
            self.lose_turn = False
        else:
            self.draw_card(random_card_list)
            self.show_inventory()


    def analyze_new_spot(self):
        spot = board[self.pos]
        if self.in_ant_loop:
            spot = ant_loop[self.pos]
        if spot[0] == 'move':
            self.move(spot[-1])
        elif spot[0] == 'aphid':
            print(f'>> get {spot[-1]} aphids')
            self.aphids += spot[-1]
        elif spot == 'mantis_pass':
            print(f'>> get a mantis pass')
            self.mantis_pass = True
        elif spot == 'mantis':
            if not self.mantis_pass:
                print(f'>> praying mantis attack! return to start')
                self.pos = 0
        elif spot == 'lose_turn':
            print(f'>> lose a turn')
            self.lose_turn = True
        elif spot == 'slide':
            print(f'>> slide across the branch to avoid the mantis')
            self.pos += 7
            self.analyze_new_spot()
        elif spot == 'home':
            print(f'{self.name} wins!')

    def face_the_ants(self, movement):
        if self.aphids >= 10:
            print(f'>> pass the ants and give them 10 aphids.')
            self.aphids -= 10
            self.pos += movement
        else:
            print(f'>> loop until you can give the ants 10 aphids.')
            self.pos = (self.pos + movement) - 27
            self.in_ant_loop = True
            self.analyze_new_spot()

    def time_to_leave_loop(self, steps):
        return self.in_ant_loop and self.pos + steps > 6


def get_players():
    players = []
    while True:
        name = input('Type your ladybug name or press enter to continue: ')
        if not name:
            return players
        ladybug = Ladybug(name)
        players.append(ladybug)


def victory_declared(players):
    for ladybug in players:
        if ladybug.pos >= 35:
            print(f'\n\nGame over.')
            return True
    return False


def main():
    print('Welcome to the Ladybug game!')
    ladybugs = get_players()
    turn = 0
    random_card_list = list(range(35))
    random.shuffle(random_card_list)
    while not victory_declared(ladybugs):
        ladybugs[turn].one_turn(random_card_list)
        input('press enter to continue')
        if turn == len(ladybugs) - 1:
            turn = 0
        else:
            turn += 1


if __name__ == '__main__':
    main()
