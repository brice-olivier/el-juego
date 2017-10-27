"""p stands for player(s). c for card(s)"""
import os
import random

map_p_c = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4}


class ElJuego(object):
    def __init__(self, nb_p):
        self.nb_p = nb_p
        self.deck = list(range(2, 100))
        self.stacks = [[1], [1], [100], [100]]
        random.shuffle(self.deck)
        self.hands = [self.deck[i*map_p_c[nb_p]:(i+1)*map_p_c[nb_p]] for i in range(0, nb_p)]
        self.deck = self.deck[nb_p*map_p_c[nb_p]:]
        first_p = random.sample(range(0, nb_p), 1)[0]
        self._start_game(first_p)

    def _start_game(self, first_p):
        print("Hi, welcome to El Juego. Collaborate with your partners and beat El Juego!")
        print("Moves are made in the form card_nb stack_id")
        print("Example: 98 3")
        print("Good luck!")
        current_p = first_p
        win = False
        nb_moves_current_p = 0
        while (self._can_play(current_p) or nb_moves_current_p >= self._nb_min_moves()) and not win:
            print("P {} - {} cards left in deck.".format(current_p, len(self.deck)), sep="")
            print("Stacks: 0: A[{}, ], 1: A[{}], 2: D[{}], 3: D[{}]".format(self.stacks[0][-1],
                                                                            self.stacks[1][-1],
                                                                            self.stacks[2][-1],
                                                                            self.stacks[3][-1]), sep="")
            print("Your hand:", self.hands[current_p])
            res = self._play(current_p, nb_moves_current_p)
            if self._is_win():
                win = True
            elif res == 1:
                nb_moves_current_p += 1
            elif res == 0:
                self._pick_c(current_p)
                current_p = self._next_p(current_p)
                nb_moves_current_p = 0
                os.system("clear")
        if win:
            print("Game over, you win.")
        else:
            print("Game over loser.")

    def _can_play(self, p):
        for c in self.hands[p]:
            if c > self.stacks[0][-1] or c == self.stacks[0][-1] - 10 \
                    or c > self.stacks[1][-1] or c == self.stacks[1][-1] - 10 \
                    or c < self.stacks[2][-1] or c == self.stacks[2][-1] + 10 \
                    or c < self.stacks[3][-1] or c == self.stacks[3][-1] + 10:
                return True
        return False

    def _nb_min_moves(self):
        if len(self.deck) == 0:
            return 1
        else:
            return 2

    def _is_valid_move(self, current_p, move):
        if not isinstance(move, tuple):
            return False
        if not all(isinstance(elem, int) for elem in move):
            return False
        if move[0] not in self.hands[current_p]:
            return False
        if move[1] not in range(0, 4):
            return False
        if move[1] == 0 or move[1] == 1:
            if move[0] > self.stacks[move[1]][-1] or move[0] == self.stacks[move[1]][-1] - 10:
                return True
        elif move[1] == 2 or move[1] == 3:
            if move[0] < self.stacks[move[1]][-1] or move[0] == self.stacks[move[1]][-1] + 10:
                return True
        return False

    def _play(self, current_p, nb_moves_current_p):
        try:
            if nb_moves_current_p >= self._nb_min_moves():
                print("Your move (x to end your turn): ", end="")
                move = input()
                if move == "x":
                    print()
                    return 0
                else:
                    move = tuple(int(x.strip()) for x in move.split(' '))
            else:
                print("Your move: ", end="")
                move = tuple(int(x.strip()) for x in input().split(' '))
            if self._is_valid_move(current_p, move):
                self.stacks[move[1]].append(move[0])
                self.hands[current_p].remove(move[0])
                print()
                return 1
        except Exception as e:
            pass
        print("\nInvalid move.")
        return -1

    def _next_p(self, current_p):
        next_p = (current_p + 1) % self.nb_p
        while len(self.hands[next_p]) == 0:
            next_p = (next_p + 1) % self.nb_p
        return next_p

    def _is_win(self):
        nb_c_left = 0
        for hand in self.hands:
            nb_c_left += len(hand)
        if len(self.deck) == 0 and nb_c_left == 0:
            return True
        return False

    def _pick_c(self, current_p):
        while len(self.hands[current_p]) < map_p_c[self.nb_p] and len(self.deck) > 0:
            self.hands[current_p].append(self.deck[0])
            self.deck = self.deck[1:]


def main():
    ElJuego(1)


if __name__ == '__main__':
    main()
