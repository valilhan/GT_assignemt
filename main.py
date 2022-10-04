# Valihan Ilyasov v.ilyasov@innopolis.university
import random

day = 14
month = 2
year = 1999

max_move = day+month
final = day+month+year


class Log:

    def __init__(self, init):
        self.log = []
        self.log.append(init)

    def append(self, move, position_to, turn):
        #  add to log additional line
        who = lambda: "You" if turn == 0 else "Bot"
        self.log.append(f"{who()} moved by {move} now position is {position_to}")

    def show(self, ):
        #  Show all logfile
        text = ""
        for line in self.log:
            print(line)
            text += line + '\n'
        #  Create or rewrite logfile
        with open('./logfile.txt', 'w') as f:
            f.write(text)


class Game:
    global max_move
    global final

    def __init__(self):
        self.log = []
        self.playing_mode = None
        self.position = None
        self.move_to = [0] * (final + 1)
        move = 1
        for i in range(final - 1, 0, -1):
            if move <= max_move:
                self.move_to[i] = move
                move += 1
            else:
                self.move_to[i] = 0
                move = 1

        self.input()

    def input(self):
        #  Read all parameters for start game

        while True:
            position = input(
                f"Start at a random(input random) or specified position(input number between [1,{final}] ? ")
            if position == 'random':
                self.position = random.randint(1, final + 1)
                break
            elif position.isdigit():
                position = int(position)
                if 1 <= position <= final:
                    self.position = position
                    break
            print("Not correct input. Input again")

        while True:
            playing_mode = input("Which mode you want to choose (input smart/random/advisor) ? ")
            if playing_mode == 'random':
                self.playing_mode = 0
                break
            elif playing_mode == 'smart':
                self.playing_mode = 1
                break
            elif playing_mode == 'advisor':
                self.playing_mode = 2
                break
            else:
                print("Not correct input. Input again")

        print('-' * 20)
        print()
        print('Your starting position ', self.position, ' Yous should reach ', final, ' to win!')
        mode = lambda x: "smart" if x == 1 else "advisor"
        print('Your playing mod is', mode(self.playing_mode))
        print()
        print('-' * 20)
        logfile = Log(f"Starting position {self.position}")
        print("\n Bot Win") if not self.play(logfile) else print("\n You win")
        while True:
            playing_mode = input("Do you want to see log file (yes/no) ? ")
            if playing_mode == 'yes':
                logfile.show()
                break
            elif playing_mode == 'no':
                break
            else:
                print("Not correct input. Input again")

        while True:
            playing_mode = input("Do you want to play again (yes/no) ? ")
            if playing_mode == 'yes':
                self.input()
                break
            elif playing_mode == 'no':
                break
            else:
                print("Not correct input. Input again")

    def play(self, logfile):
        turn = 0  # by default your turn to move first
        while self.position != final:
            if turn == 0:
                # User turn
                while True:
                    # Hint for user if playing mode advisor
                    advise_string = lambda \
                            x: f"\n (to win you should move by +{self.move_to[self.position]}) " if x == 2 and \
                                                                                                    self.move_to[
                                                                                                        self.position] != 0 else ""

                    print('-' * 20)
                    move = input(
                        f"Your position {self.position} move by (input number between [1, {max_move}]) {advise_string(self.playing_mode)}")
                    print('-' * 20)
                    if move.isdigit():
                        move = int(move)
                        if 1 <= move <= max_move:
                            if self.position + move > final:
                                print("You cannot reach this position!")
                                continue
                            self.position += move
                            logfile.append(move, self.position, turn)
                            break
                    else:
                        print("Not correct input. Input again")
                turn = 1
            else:
                # Bot turn
                move_random = random.randint(1, min(max_move, final - self.position))  # random move if playing mode
                # is random
                move_smart = lambda x: self.move_to[x] if self.move_to[x] != 0 else move_random  # move with using
                # list move_to or if move_to use not possible do random move
                move = lambda x: move_smart(self.position) if x == 1 or x == 2 else move_random  # Choose a move
                # dependent on playing move random or smart/advisor
                bot_move = move(self.playing_mode)
                print('-' * 20)
                print(f"Bot move by {bot_move}", end=" ")
                self.position += bot_move
                logfile.append(bot_move, self.position, turn)
                print(f"position is {self.position}")
                print('-' * 20)
                turn = 0
        return turn


if __name__ == '__main__':
    # Start play game
    game = Game()
