import tkinter
import random
import sys
import copy
import math
from colour import Color

# these are for the game
cols = 9
rows = 9
numMines = 26
visual = True  # does screen show up
minesPlaced = 0  # how many mines placed in setup
mines = []  # -1 is for blank, -2 is blank flag, -3 is for mine, -4 is for mine flag and other for # nearby
squares = []  # stores the buttons
wins = 0  # games won
losses = 0  # games lost
playing = True  # if should restart
sys.setrecursionlimit(100)  # avoid errors with recursion for massive windows
clicked = 0  # how many open squares left to click
size = 1300
# for the bot
info_map = []  # x,y (>0-the number, -1-info, -2-unknown, -3 mine)
auto_mode = 2  # 0 nothing, 1 obvious, 2 certains, 3 guessing
hide_percents = False
first_click_zero = True
alive_chance = 1
# colors = list(Color("Green").range_to(Color("Red"), 10))

# testing
# odds_array = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

def create():
    global minesLeft, root  # mines not flagged and tkinter window
    if visual:
        root = tkinter.Tk()  # Main window
        root.title('Minesweeper')
        minesLeft = tkinter.StringVar()  # allow to attach to button
    prepareWindow()
    if visual:
        root.mainloop()


def prepareWindow():  # sets up window
    global rows, cols, squares, mines, numMines, minesPlaced, clicked, info_map, alive_chance, size
    alive_chance = 1
    mines = []  # resets mines
    info_map = []  # resets info_map
    minesPlaced = numMines
    clicked = rows*cols-numMines
    for px in range(0, rows):  # set up mines array with blank things
        mines.append([])
        info_map.append([])
        for py in range(0, cols):
            info_map[px].append(-2)  # set up inf map all unknown tiles
            mines[px].append(-1)  # -1 is for blank, -2 is blank flag, -3 is for mine, -4 is for mine flag and other for # nearby
    if visual:
        squares = []  # sets up window first options then mines
        tkinter.Label(root, textvariable=minesLeft).grid(row=0, column=0, columnspan=int(cols / 4), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        minesLeft.set(str(numMines))
        cur = int(cols / 4)  # formatting for which  column to be in
        tkinter.Label(root, text="Wins: " + str(wins) + " Losses: " + str(losses)).grid(row=0, column=cur, columnspan=int((cols / 4) + 0.25), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # Creates settings Button
        cur += int((cols / 4) + 0.25)
        tkinter.Button(root, text='Settings', command=settings).grid(row=0, column=cur, columnspan=int((cols / 4) + 0.5), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # Creates settings Button
        cur += int((cols / 4) + 0.5)
        tkinter.Button(root, text='Restart', command=restart).grid(row=0, column=cur, columnspan=int((cols / 4) + 0.75), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # Creates restart Button
        for px in range(0, rows):  # making all the buttons
            squares.append([])
            for py in range(0, cols):
                f = tkinter.Frame(root, height=int(size / max(2 * rows, cols)), width=int(size / max(2 * rows, cols)))  # Frame for each button to get nice size
                b = tkinter.Button(f, text='', foreground='black', font=("Helvetica", int((size/2) / max(2 * rows, cols)), "bold"), background='gray')
                b.bind("<Button-1>", lambda e, x=px, y=py: click(x, y))
                b.bind("<Button-3>", lambda e, x=px, y=py: rClick(x, y))
                f.pack_propagate(0)  # doesn't change size
                f.grid(row=px + 1, column=py, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
                b.pack(fill='both', expand=1)
                squares[px].append(b)
        tkinter.Button(root, text='Iterate', command=iterate).grid(row=rows+2, column=0, columnspan=int((cols/2)+0.5), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)  # Creates restart Button
        tkinter.Button(root, text='simulate Game', command=simulate).grid(row=rows+2, column=int((cols/2)+0.5), columnspan=int(cols/2), sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
        # mines[0][0] = -3
        # mines[0][3] = -3
        # mines[1][0] = -3
        # mines[1][2] = -3
        # mines[1][3] = -3
        # mines[2][1] = -3
        # mines[2][3] = -3
        # minesPlaced = 0
        # click(2, 0)
        # click(2, 2)
        # click(3, 0)
        # click(3, 1)
        # click(3, 2)
        # click(3, 3)
        # click(3, 4)
        # click(2, 4)
        # click(1, 4)
        # click(0, 4)
        # rClick(0, 3)
        # rClick(1, 3)
        # rClick(2, 1)
        # rClick(2, 3)


def click(x, y):
    global mines, squares, playing, minesPlaced, clicked
    if playing:
        for px in range(0, len(mines)):
            for py in range(0, len(mines[0])):
                if (info_map[px][py] == -1 or info_map[px][py]  == -2):
                    squares[px][py]['text'] = ""
        while minesPlaced != 0:  # places mines if not placed before
            px = random.randint(0, len(mines) - 1)
            py = random.randint(0, len(mines[0]) - 1)
            if not (mines[px][py] < -2):  # checking if random square can place a mine here
                if first_click_zero:
                    if not ((px == x or px == x+1 or px == x-1) and (py == y or py == y+1 or py == y-1)):
                        mines[px][py] -= 2
                        minesPlaced -= 1
                else:
                    if not(px == x and py == y):
                        mines[px][py] -= 2
                        minesPlaced -= 1
        if mines[x][y] == -3:  # what to do if click mine
            playing = False
            print("you lost, Record: " + str(wins) + "-" + str(losses+1)+" CL: "+str(clicked) + " Alive Chance: "
                  + str(alive_chance))
            if visual:
                for px in range(0, len(mines)):
                    for py in range(0, len(mines[0])):
                        if mines[px][py] < -2:
                            squares[px][py].config(background='red')
                        elif mines[px][py] == -1 or mines[px][py] == -2:
                            squares[px][py].config(background='gray')  # if bot changed background back to gray
        else:
            if mines[x][y] > -1:  # what to do if click number
                # print("number was clicked"+str(x)+str(y))
                if mines[x][y] == getNum(x, y, -2, -4, mines):  # if mines around equals flags around
                    for cx in range(x - 1, x + 2):
                        for cy in range(y - 1, y + 2):
                            if -1 < cx < len(mines) and -1 < cy < len(mines[0]) and (mines[cx][cy] == -1 or mines[cx][cy] == -3) and not (cx == x and cy == y):
                                click(cx, cy)
            else:
                if mines[x][y] == -1 or mines[x][y] == -3:  # if click a non flagged gray
                    mines[x][y] = getNum(x, y, -3, -4, mines)
                    clicked -= 1
                    info_map[x][y] = mines[x][y]  # if click then become known cell
                    for i in range(x-1, x+2):
                        for j in range(y-1, y+2):
                            if -1 < i < len(mines) and -1 < j < len(mines[0]):
                                if info_map[i][j] == -2:
                                    info_map[i][j] = -1  # cells become info squares
                                elif info_map[i][j] == -3:
                                    info_map[x][y] -= 1
                    if info_map[x][y] < 0:
                        info_map[x][y] = 0
                    if clicked == 0:  # checks if you won
                        playing = False
                        print("you won,  Record: " + str(wins + 1) + "-" + str(losses) + "Alive Chance: " + str(alive_chance))
                    if mines[x][y] == 0:  # autoclick others
                        squares[x][y]['text'] = ""
                        for cx in range(x - 1, x + 2):
                            for cy in range(y - 1, y + 2):
                                if -1 < cx < len(mines) and -1 < cy < len(mines[0]) and (mines[cx][cy] == -3 or mines[cx][cy] == -1) and not (cx == x and cy == y):
                                    click(cx, cy)
                    if visual:
                        squares[x][y].config(background='white')
                        squares[x][y]['state'] = 'disabled'
                        squares[x][y].config(relief=tkinter.SUNKEN)
                        if mines[x][y] > 0:
                            squares[x][y]['text'] = str(mines[x][y])


def getNum(x, y, c, c2, array):  # gets number of c and c2 nearby
    num = 0
    for cx in range(x - 1, x + 2):
        for cy in range(y - 1, y + 2):
            if -1 < cx < len(array) and -1 < cy < len(array[0]) and (array[cx][cy] == c or array[cx][cy] == c2):
                num += 1
    return num


def rClick(x, y):
    if mines[x][y] == -3:  # flag a mine
        mines[x][y] = -4
        if visual:
            squares[x][y]['text'] = '?'
            changeML(-1)
    else:
        if mines[x][y] == -1:  # flag a not mine
            mines[x][y] = -2
            if visual:
                squares[x][y]['text'] = '?'
                changeML(-1)
        else:  # Same for unflaging
            if mines[x][y] == -4:
                mines[x][y] = -3
                if visual:
                    squares[x][y]['text'] = ''
                    changeML(1)
            else:
                if mines[x][y] == -2:
                    mines[x][y] = -1
                    if visual:
                        squares[x][y]['text'] = ''
                        changeML(1)
    info_flag(x, y)
    if mines[x][y] < 0:  # get rid of color
        squares[x][y].config(background="Gray")


def info_flag(x, y):
    if info_map[x][y] == -1 or info_map[x][y] == -2:  #  flag it
        info_map[x][y] = -3
    elif info_map[x][y] == -3:  # unflag it
        info_map[x][y] = -1
    for rx in range(x-1, x+2):
        for ry in range(y-1, y+2):
            if -1 < rx < len(mines) and -1 < ry < len(mines[0]) and info_map[rx][ry] > -1:
                info_map[rx][ry] = mines[rx][ry]
                for px in range(rx - 1, rx + 2):
                    for py in range(ry - 1, ry + 2):
                        if -1 < px < len(mines) and -1 < py < len(mines[0]) and info_map[px][py] == -3:
                            info_map[rx][ry] -= 1
                if info_map[rx][ry] < 0:
                    info_map[rx][ry] = 0


def settings():  # settings window creation
    global rows, cols, numMines
    s = tkinter.Tk()
    tkinter.Label(s, text='Columns:').grid(row=-0, column=0)
    tkinter.Label(s, text='Rows:').grid(row=1, column=0)
    tkinter.Label(s, text='Mines:').grid(row=2, column=0)
    e1 = tkinter.Entry(s)
    e2 = tkinter.Entry(s)
    e3 = tkinter.Entry(s)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    tkinter.Button(s, text='Enter', command=lambda: enter(e1, e2, e3, s)).grid(row=3, columnspan=2, sticky=tkinter.N + tkinter.W + tkinter.S + tkinter.E)
    e1.insert(0, str(cols))
    e2.insert(0, str(rows))
    e3.insert(0, str(numMines))
    s.mainloop()


def enter(e1, e2, e3, s):
    global rows, cols, numMines
    cols = int(e1.get())
    rows = int(e2.get())
    numMines = int(e3.get())
    if cols < 4:
        cols = 4
    if rows < 3:
        rows = 3
    if numMines > rows*cols-9:
        numMines = rows*cols-9
    if numMines < 0:
        numMines = 0
    s.destroy()


def restart():
    global playing, wins, losses
    if clicked == 0:
        wins += 1
    else:
        if playing:
            print("you lost, Record: " + str(wins) + "-" + str(losses + 1))
        losses += 1
    if visual:
        for x in root.winfo_children():
            x.destroy()
    prepareWindow()
    playing = True


def changeML(x):
    global minesLeft
    minesLeft.set(str(int(str(minesLeft.get()))+x))


# -1 is for blank, -2 is blank flag, -3 is for mine, -4 is for mine flag and other for # nearby
def iterate():  # this is the bot
    global alive_chance
    # print("info map: " + str(info_map))
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if mines[x][y] < 0:
                squares[x][y].config(background="gray")
                if info_map[x][y] == -1 or info_map[x][y] == -2:
                    squares[x][y]["text"] = ""
    if minesPlaced != 0:
        if auto_mode > 0:
            click(int(len(mines)/2), int(len(mines[0])/2))
        else:
            squares[int(len(mines)/2)][int(len(mines[0])/2)].config(background="Light Green")
        return
    change = flag_check()
    change = click_check() or change  # any obvious click or flags it also avoids error of info map with 0's
    if not change:
        ops = get_ops()
        temp_count = 0  # min mines of all ops
        # this is all for the print
        for x in range(len(mines)):
            for y in range(len(mines[0])):
                if ops[0][0][x][y]:
                    temp_count += 1
        # print_text = "num of mines: options "
        # for i in range(len(ops)):
        #     print_text += str(temp_count + i) + ": " + str(len(ops[i])) + ", "
        # print(print_text)
        # ops = delete_impossible(ops)
        # temp_count = 0  # min mines of all ops
        # for x in range(len(mines)):
        #     for y in range(len(mines[0])):
        #         if ops[0][0][x][y]:
        #             temp_count += 1
        # print_text = "num of mines: options "
        # for i in range(len(ops)):
        #     print_text += str(temp_count + i) + ": " + str(len(ops[i])) + ", "
        # print(print_text)
        if not check_certains(ops): # checks for cells that are either in all or none of the opps
            if not display_ods(ops):
                spot = guess(ops, 0)
                print("Guessing: " + str(spot))
                alive_chance *= (100-int(squares[spot[0]][spot[1]]["text"]))/100
                if auto_mode > 2:
                    click(spot[0], spot[1])
                else:
                    squares[spot[0]][spot[1]].config(background="light green")
                if hide_percents:
                    for x in squares:
                        for y in x:
                            try:
                                if int(y["text"]) > 8:
                                    y["text"] = ""
                            except ValueError:
                                pass
                # # testing
                # odds_array[odds_place][1] += 1
                # if playing:
                #     odds_array[odds_place][0] += 1
                # string = ""
                # for i in range(len(odds_array)):
                #     try:
                #         string += str((20-i)*5) + ":" + str(odds_array[i][0]/odds_array[i][1]) + ", "
                #     except ZeroDivisionError:
                #         string += "N/A, "
                # print(string)





def flag_check():
    change = False
    for x in range(0, len(mines)):
        for y in range(0, len(mines[0])):
            if info_map[x][y] > 0 and info_map[x][y] == getNum(x, y, -1, -1, info_map):
                for rx in range(x - 1, x + 2):
                    for ry in range(y - 1, y + 2):
                        if -1 < rx < len(mines) and -1 < ry < len(mines[0]) and info_map[rx][ry] == -1:
                            if auto_mode > 0:
                                rClick(rx, ry)
                            else:
                                squares[rx][ry].config(background="Pink")
                            change = True
    return change


def click_check():  # could be made faster if done with mines
    change = False
    for x in range(0, len(mines)):
        for y in range(0, len(mines[0])):
            if info_map[x][y] == 0:
                for rx in range(x - 1, x + 2):
                    for ry in range(y - 1, y + 2):
                        if -1 < rx < len(mines) and -1 < ry < len(mines[0]) and info_map[rx][ry] == -1:
                            # print("Click: " + str(rx) + ", " + str(ry))
                            change = True
                            if auto_mode > 0:
                                click(rx, ry)
                            else:
                                squares[rx][ry].config(background="Light Green")
                            change = True
    return change


def get_ops():
    ops = []
    over = False
    cur_opp = []
    min_mines = 0
    for x in range(len(mines)):
        cur_opp.append([])
        for y in range(len(mines[0])):
            cur_opp[x].append(False)
    pos = [0, 0]
    while not over:
        while pos[0] < len(mines):
            while pos[1] < len(mines[0]):
                if info_map[pos[0]][pos[1]] == -1:
                    action = check_valid(pos, cur_opp)  # 0 = make mine, 1 = continue, 2 = needs to be mine3 = go back
                    if action == 0 or action == 2:
                        cur_opp[pos[0]][pos[1]] = True
                    elif action == 3:
                        new = go_back(pos, cur_opp)
                        # print("new: " + str(new))
                        if not new:
                            return ops
                        else:
                            pos = new[0]
                            cur_opp = new[1]
                pos[1] += 1
            pos[0] += 1
            pos[1] = 0
        temp_count = 0
        for x in range(len(mines)):
            for y in range(len(mines[0])):
                if cur_opp[x][y]:
                    temp_count += 1
        # print("Temp Count: " + str(temp_count) + " Min mines: " + str(min_mines) + " Cur opp: " + str(cur_opp))
        # temp count is num mines in pos
        # min mines is the  num mines in the pos with least mines
        if temp_count >= min_mines:  # not a new min mines
            if min_mines != 0:
                for dif in range(temp_count-min_mines-len(ops)+1):  # add gaps if multiple gap to min mines
                    ops.append([])
            else:
                min_mines = temp_count  # this runs the first time and sets the min
                ops.append([])
            ops[temp_count-min_mines].append(copy.deepcopy(cur_opp))
        else:
            ops.insert(0, [copy.deepcopy(cur_opp)])
            for dif in range(min_mines-temp_count-1):  # how many extras to add at the start:
                ops.insert(1, [])
            min_mines = temp_count
        # print("New Ops: " + str(cur_opp))
        # this is all for the print
        temp_count = 0
        for x in range(len(mines)):
            for y in range(len(mines[0])):
                if ops[0][0][x][y]:
                    temp_count += 1
        # # print_text = "num of mines: options "
        # for i in range(len(ops)):
        #     print_text += str(temp_count + i) + ": " + str(len(ops[i])) + ", "
        # print(print_text)
        new = go_back(pos, cur_opp)  # goes back to an earlier pos cause finished
        # print("new: " + str(new))
        if not new:
            return ops
        else:
            pos = new[0]
            cur_opp = new[1]
            if pos[1] < len(mines[0]) - 1:
                pos[1] += 1
            else:
                pos[1] = 0
                pos[0] += 1


def check_valid(pos, cur_opp):
    x = pos[0]
    y = pos[1]
    action = 0  # 0 is unknown, 1 is dont make mine, 2 is make mine, 3 is go back
    for rx in range(x-1, x+2):
        for ry in range(y-1, y+2):
            if -1 < rx < len(mines) and -1 < ry < len(mines[0]) and info_map[rx][ry] > 0:  # if it is a known number
                if action == 0:
                    max_count = 1  # max number of mines around, this included
                    min_count = 0
                elif action == 1:
                    max_count = 0
                    min_count = 0  # min number of mines around number, this not included
                elif action == 2:
                    max_count = 1
                    min_count = 1
                for cx in range(rx-1, rx+2):
                    for cy in range(ry-1, ry+2):
                        if -1 < cx < len(mines) and -1 < cy < len(mines[0]) and info_map[cx][cy] == -1:
                            if cur_opp[cx][cy]:
                                min_count += 1
                                max_count += 1
                            elif cx > x or (cx == x and cy > y):
                                max_count += 1
                if min_count >= info_map[rx][ry]:
                    if min_count > info_map[rx][ry]:
                        return 3
                    elif action != 2:
                        action = 1
                elif max_count <= info_map[rx][ry]:
                    if max_count < info_map[rx][ry]:
                        return 3
                    elif action != 1:
                        action = 2
    return action


def go_back(pos, cur_opp):
    while pos[0] > -1:
        pos[1] -= 1
        while pos[1] > -1:
            # print("Going back from " + str(pos))
            if cur_opp[pos[0]][pos[1]]:
                # print("Removed: " + str(pos))
                cur_opp[pos[0]][pos[1]] = False
                if check_remove(pos, cur_opp):
                    return pos, cur_opp
            pos[1] -= 1
        pos[1] = len(mines[0])  # go to end will be -1 before next math
        pos[0] -= 1
    return False


def check_remove(pos, cur_opp):
    x = pos[0]
    y = pos[1]
    for rx in range(x - 1, x + 2):
        for ry in range(y - 1, y + 2):
            if -1 < rx < len(mines) and -1 < ry < len(mines[0]) and info_map[rx][ry] > 0:  # if it is a known number
                max_count = 0  # max number of mines around number, this not included
                for cx in range(rx - 1, rx + 2):
                    for cy in range(ry - 1, ry + 2):
                        if -1 < cx < len(mines) and -1 < cy < len(mines[0]) and info_map[cx][cy] == -1:
                            if cur_opp[cx][cy]:
                                max_count += 1
                            elif cx > x or (cx == x and cy > y):  #if the information square is later then the max is more
                                max_count += 1
                # print("Trying to remove (" + str(x) + ", " + str(y) + ") Analyzing (" + str(rx) + ", " + str(ry) +
                #       ") Max: " + str(max_count) + " needs to be less than: " + str(info_map[rx][ry]))
                if max_count < info_map[rx][ry]:
                    return False
    return True


def check_certains(ops):
    change = False
    if auto_mode > 1:  # crete array for where to click because or else info map changes during
        clicks = []
        rclicks = []
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if info_map[x][y] == -1:
                click_it = True
                flag_it = True
                for i in range(len(ops)):
                    for p in range(len(ops[i])):
                        if ops[i][p][x][y]:
                            click_it = False
                        else:
                            flag_it = False
                if click_it:
                    change = True
                    if auto_mode > 1:
                        # print("Clicking: (" + str(x) + ", " + str(y) + ")")
                        clicks.append([x, y])
                    else:
                        squares[x][y].config(background="light green")
                elif flag_it:
                    change = True
                    if auto_mode > 1:
                        rclicks.append([x, y])
                    else:
                        squares[x][y].config(background="pink")
    if auto_mode > 1:
        for i in clicks:
            click(i[0], i[1])
        for i in rclicks:
            rClick(i[0], i[1])
    return change


def delete_impossible(ops):
    total_mines = int(minesLeft.get())  # mines not flagged in game
    unknown = 0  # number of squares no info
    min_mines = 0  # ops with min mines in info squares
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if info_map[x][y] == -2:
                unknown += 1
            if ops[0][0][x][y]:
                min_mines += 1
    ops = ops[:total_mines - min_mines + 1]  # get rid of ops with too few mines
    if total_mines - min_mines - unknown > 0:
        # print("Cutting for too few mines")
        ops = ops[total_mines - min_mines - unknown:]
    return ops


def display_ods(ops):
    global minesLeft
    change = False
    # print("ops: " + str(ops))
    unknown = 0  # number of squares no info
    min_mines = 0  # ops with min mines in info squares
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if info_map[x][y] == -2:
                unknown += 1
            if ops[0][0][x][y]:
                min_mines += 1
    total_mines = int(minesLeft.get())  # mines not flagged in game
    # print("n: " + str(unknown) + " k:" + str(total_mines-min_mines))
    multipliers = []
    for i in range(len(ops)-1):
        try:
            multiple = (unknown-total_mines+min_mines+i+1)/(total_mines-min_mines-i)
        except ZeroDivisionError:
            # this is a patchwork fix for when the minimum mines in the info cells equals the 
            # number of mines left in the game, hopefully it doesnt break anything
            multiple = 1
            break
        multipliers.append(multiple)
        for b in range(i):
            multipliers[b] *= multiple
    multipliers.append(1)
    total = 0  # this is what num would be if 100% a mine
    for i in range(len(multipliers)):
        total += multipliers[i] * len(ops[i])
    # print("Multipliers: " + str(multipliers))
    # print("Total: " + str(total))
    average_mines = 0
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if info_map[x][y] == -1:
                square_sum = 0
                for i in range(len(multipliers)):
                    for p in range(len(ops[i])):
                        if ops[i][p][x][y]:
                            square_sum += multipliers[i]
                squares[x][y]["text"] = str(math.floor((square_sum/total)*100))
                average_mines += square_sum/total
    if unknown > 0:  # only do extra stuff if any unkown squares
        if average_mines == total_mines:  # not sure if needed for rounding errors
            click_unkown(True)
            change = True
        elif average_mines + unknown == total_mines:
            change = True
            click_unkown(False)
        else:
            for x in range(len(mines)):
                for y in range(len(mines[0])):
                    if info_map[x][y] == -2:
                        squares[x][y]["text"] = str(math.floor(((total_mines-average_mines)/unknown)*100))
    return change


def click_unkown(do_click):
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if mines[x][y] < 0:
                squares[x][y].config(background="gray")
                if info_map[x][y] == -1 or info_map[x][y] == -2:
                    squares[x][y]["text"] = ""
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if info_map[x][y] == -2:
                if do_click:
                    if auto_mode > 1:
                        click(x, y)
                    else:
                        squares[x][y].config(background="Light Green")
                else:
                    if auto_mode > 1:
                        rClick(x, y)
                    else:
                        squares[x][y].config(background="pink")


def guess(ops, min_at_least):
    minimum = 100
    dont_stop = False
    # print("Minimum: " + str(min_at_least))
    for x in range(len(mines)):
        for y in range(len(mines[0])):
            if (info_map[x][y] == -1 or info_map[x][y] == -2) and minimum > int(squares[x][y]["text"]) > min_at_least:
                minimum = int(squares[x][y]["text"])
                dont_stop = True
                # print("Minimum is now: " + str(minimum))
    if dont_stop:
        min_unknowns = 8
        best_square = []
        for x in range(len(mines)):
            for y in range(len(mines[0])):
                if (info_map[x][y] == -1 or info_map[x][y] == -2) and int(squares[x][y]["text"]) == minimum:
                    # print("trying: " + str(x) + ", " + str(y))
                    go = False
                    unknowns = getNum(x, y, -2, -2, info_map)
                    # print("min_unknowns: "+str(min_unknowns))
                    if unknowns == 0:
                        be_dif = -1
                        for i in range(0, len(ops)):
                            for j in range(0, len(ops[i])):  # redoing one test but simpler
                                if not ops[i][j][x][y]:  # only if this square isnt a mine in ops
                                    # print("be_same: " + str(getNum(x, y, True, True, ops[i][j])))
                                    if be_dif == -1:
                                        be_dif = getNum(x, y, True, True, ops[i][j])
                                    elif be_dif != getNum(x, y, True, True, ops[i][j]):
                                        # print("should break")
                                        go = True
                                        break  # not perfect but whatever cuase only breaks to other amount of mines
                        if go:
                            min_unknowns = 0
                            best_square = [x, y]
                    elif unknowns < min_unknowns:
                        min_unknowns = unknowns
                        best_square = [x, y]
        if len(best_square) > 0:
            return best_square
        else:
            return guess(ops, minimum)
    else: # if no clicks give any info
        best_square = []
        for x in range(len(mines)):
            for y in range(len(mines[0])):
                if (info_map[x][y] == -1 or info_map[x][y] == -2) and minimum > int(
                        squares[x][y]["text"]):
                    minimum = int(squares[x][y]["text"])
                    best_square = [x, y]
        return best_square



def simulate():
    global auto_mode
    auto_mode = 3
    while True:
        while playing:
            iterate()
        restart()

create()
