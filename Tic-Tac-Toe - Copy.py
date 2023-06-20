

"""
Tic Tac Toe : Compete against a bot that learnt from you!
=========================================================

Tic Tac Toe is  is a paper-and-pencil game for two players,
X and O, who take turns marking the spaces in a 3�3 grid.
The player who succeeds in placing three of their marks
in a horizontal, vertical, or diagonal row wins the game.


Board :-
========

    1 | 2 | 3
    ---------
    4 | 5 | 6
    ---------
    7 | 8 | 9

Constants :-
============

    win_conditions  :   List of all possible winning situations
    PATH            :   Directory, for freeze mode

Variables :-
============

    TRAIN_ITERATIONS:   Number of iterations for training set

    train           :   Flag for training mode
                        True: Yes, False: No
    PLAYER_TURN      :   Flag for who's turn it is.
                        True: Player 1, False: Player 2
    chance          :   Stores move number
    selected        :   List of all selected moves
                        Even indices for Player 1, Odd indices for Player 2

Methods :-
==========

    init_buttons     :   Connect all python methods with .ui file
    disp            :   Places the appropriate move image (cross/ circle),
                        adds move to selected and checks current board state
    check           :   Analyzes current board state for outcome
    play_move        :   Finds the most winning move based on prior knowledge
    test_lose        :   Helper function for play_move to play a move if next move
                        stops a lose or is a guaranteed win
    train_data       :   Enters training mode where the bot is allowed to play
                        with itself for N_ITERATIONS finding new moves
    store_data       :   Stores the current set of moves with outcome to dataset.csv
    reset_data       :   Clears all data history making the AI dumb
    disable         :   Temporarily lock down all buttons after successful outcome
    reset           :   Resets current board and re-initializes variables


Dependencies :-
===============

    dataset.csv     :   Labelled history of moves played
    GUI.ui          :   ui format of GUI used loaded in variable "ui"
    cross.jpg       :   Player 1 move
    circle.jpg      :   Player 2 move
    def.jps         :   White tile of same size as cross/circle
    icon            :   Window icon for the application

"""

import sys
import csv
import random
from PyQt5 import QtWidgets, QtGui, QtCore, uic

win_conditions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7],
                  [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
train = False       # Play mode
PATH = 'C://Users//bull//Desktop//TicTacToe-master//data//'     # PATH for dependencies


def reset():
    global chance, selected
    chance = 0      # Move number
    selected = []   # Moves played

    ui.pushButton_1.setEnabled(True)
    ui.pushButton_2.setEnabled(True)
    ui.pushButton_3.setEnabled(True)
    ui.pushButton_4.setEnabled(True)
    ui.pushButton_5.setEnabled(True)
    ui.pushButton_6.setEnabled(True)
    ui.pushButton_7.setEnabled(True)
    ui.pushButton_8.setEnabled(True)
    ui.pushButton_9.setEnabled(True)

    ui.pushButton_1.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_2.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_3.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_4.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_5.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_6.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_7.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_8.setIcon(QtGui.QIcon(PATH+'def.jpg'))
    ui.pushButton_9.setIcon(QtGui.QIcon(PATH+'def.jpg'))

    ui.pushButton_1.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_2.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_3.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_4.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_5.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_6.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_7.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_8.setIconSize(QtCore.QSize(175, 175))
    ui.pushButton_9.setIconSize(QtCore.QSize(175, 175))

    ui.label_1.setText("Your Turn")


def disable():
    global train, PLAYER_TURN
    if not train:       # Not in training phase
        ui.pushButton_1.setEnabled(False)
        ui.pushButton_2.setEnabled(False)
        ui.pushButton_3.setEnabled(False)
        ui.pushButton_4.setEnabled(False)
        ui.pushButton_5.setEnabled(False)
        ui.pushButton_6.setEnabled(False)
        ui.pushButton_7.setEnabled(False)
        ui.pushButton_8.setEnabled(False)
        ui.pushButton_9.setEnabled(False)
    else:
        PLAYER_TURN = True


def disp(self, select):
    global chance

    if chance % 2 == 0:             # Player 1
        self.setIcon(QtGui.QIcon(PATH+'cross.jpg'))
    else:                           # Player 2
        self.setIcon(QtGui.QIcon(PATH+'circle.jpg'))
    self.setIconSize(QtCore.QSize(175, 180))

    chance += 1
    selected.append(select)
    check()


def check():
    global selected, win_conditions, chance

    player_1 = [selected[i] for i in range(0, len(selected), 2)]      # Player 1 moves
    player_2 = [selected[i+1] for i in range(0, len(selected)-1, 2)]  # Player 2 moves

    for x in win_conditions:
        if set(player_1) >= set(x):
            ui.label_1.setText("Player 1 Wins!")
            store_data("L")              # Bot loses
            disable()
            return
        elif set(player_2) >= set(x):
            ui.label_1.setText("Player 2 Wins!")
            store_data("W")              # Bot wins
            disable()
            return

    if len(selected) == 9:
        ui.label_1.setText("Draw!")
        store_data("D")                  # Draw situation
        return

    if chance % 2 == 1:     # Bot to play
        x = play_move()
        exec("disp(ui.pushButton_%d, %d)" % (x, x))


def play_move():
    global selected, win_conditions, chance, PATH

    player_1 = [selected[i] for i in range(0, len(selected), 2)]
    player_2 = [selected[i + 1] for i in range(0, len(selected) - 1, 2)]

    k = test_lose(player_2, player_1)        # Find Win Move
    if k == 99:
        k = test_lose(player_1, player_2)    # Find Force Move
        if k == 99:
            # No win/force move, find best move from dataset

            avail = [x for x in [1, 2, 3, 4, 5, 6, 7, 8, 9] if x not in selected]
            move_res = {x: 0 for x in avail}  # dictionary with all moves and outcome probability

            with open(PATH + 'dataset.csv', mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                line_count = 0

                for row in csv_reader:
                    if line_count == 0:         # Ignore header
                        line_count += 1
                        continue

                    temp = [x for x in row[:-1] if int(x) not in selected]
                    while '0' in temp:          # Remove blank moves
                        del temp[-1]

                    if len(temp) > 0:
                        if row[chance] == temp[0]:
                            if row[-1] == 'W':
                                move_res[int(temp[0])] += 1
                            elif row[-1] == 'D':
                                move_res[int(temp[0])] += 0.5
                            elif row[-1] == 'L':
                                move_res[int(temp[0])] -= 1
                        else:
                            move_res[int(random.choice(temp))] += 0.5
                    else:
                        move_res[random.choice(avail)] -= 0.5

            if chance % 2 == 0:  # Player 1
                move_avail = [x for x in move_res
                              if move_res[x] == move_res[max(move_res, key=move_res.get)]]  # max
            else:               # Player 2
                move_avail = [x for x in move_res
                              if move_res[x] == move_res[min(move_res, key=move_res.get)]]  # min
            x = random.choice(move_avail)

            # x = max(move_res, key=move_res.get)

        else:
            x = k
    else:
        x = k
    return x


def test_lose(player_1, player_2):
    global selected

    for x in win_conditions:
        if len(set(x)-set(player_1)) < 2 and list(set(x) - set(player_1))[0] not in player_2:    # Check if next move is win/ force
            return list(set(x) - set(player_1))[0]

    return 99


def store_data(outcome):
    global selected
    with open(PATH + 'dataset.csv', mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(9 - len(selected)):
            selected.append(0)
        csv_writer.writerow(
            [str(selected[0]), str(selected[1]), str(selected[2]), str(selected[3]), str(selected[4]),
             str(selected[5]), str(selected[6]), str(selected[7]), str(selected[8]), outcome])


def train_data():
    global train, PLAYER_TURN
    train_iterations = 200      # Variable for number of train sets
    reset()          # Reset board for any moves
    train = True     # Set train flag
    msg = QtWidgets.QMessageBox()
    msg.setText("Training data, please wait few minutes till you get next prompt...")
    msg.exec()
    for _ in range(train_iterations):
        PLAYER_TURN = False
        for _ in range(5):
            if not PLAYER_TURN:
                move = play_move()
                # exec("disp(ui.pushButton_%d, %d)" % (x, x))
                __ = getattr(disp, f'ui.pushButton_{move}, {move}')
        reset()
    msg.setText("Trained Successfully!")
    msg.exec()
    train = False   # Reset train flag


def reset_data():
    with open(PATH + 'dataset.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["chance1", "chance2", "chance3", "chance4", "chance5",
                             "chance6", "chance7", "chance8", "chance9", "outcome"])

    msg = QtWidgets.QMessageBox()
    msg.setText("Reset complete, enjoy your free wins!")
    msg.exec()


def init_buttons():
    reset()

    ui.pushButton_1.clicked.connect(lambda x: disp(ui.pushButton_1, 1) if 1 not in selected else 0)
    ui.pushButton_2.clicked.connect(lambda x: disp(ui.pushButton_2, 2) if 2 not in selected else 0)
    ui.pushButton_3.clicked.connect(lambda x: disp(ui.pushButton_3, 3) if 3 not in selected else 0)
    ui.pushButton_4.clicked.connect(lambda x: disp(ui.pushButton_4, 4) if 4 not in selected else 0)
    ui.pushButton_5.clicked.connect(lambda x: disp(ui.pushButton_5, 5) if 5 not in selected else 0)
    ui.pushButton_6.clicked.connect(lambda x: disp(ui.pushButton_6, 6) if 6 not in selected else 0)
    ui.pushButton_7.clicked.connect(lambda x: disp(ui.pushButton_7, 7) if 7 not in selected else 0)
    ui.pushButton_8.clicked.connect(lambda x: disp(ui.pushButton_8, 8) if 8 not in selected else 0)
    ui.pushButton_9.clicked.connect(lambda x: disp(ui.pushButton_9, 9) if 9 not in selected else 0)

    ui.pushButton_new.clicked.connect(reset)
    ui.pushButton_train.clicked.connect(train_data)
    ui.pushButton_reset.clicked.connect(reset_data)


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        PATH = sys._MEIPASS+'//data//'

    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon('icon.jpg'))
    ui = uic.loadUi("C://Users//bull//Desktop//TicTacToe-master//data//GUI.ui")

    init_buttons()

    ui.show()
    app.exec()
