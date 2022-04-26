__author__ = 'philippe'
from turtle import width
from Tkinter import *
master = Tk()

triangle_size = 0.1
cell_score_min = -0.2
cell_score_max = 0.2
Width = 100
(x, y) = (5, 5)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player_M = (2, y-1)
player_M_block = False
player_F = (2,0)
player_F_block =False
score = 1
restart = False
walk_reward = -1

specials = [[1, 3, "blue", 13, 10]]#(1, 3, "green", 13)
drop_off = [[2, 2, "green", 13, 0], [0,0,"green", 13, 0]]

cell_scores = {}


def create_triangle(i, j, action):
    if action == actions[0]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+triangle_size)*Width,
                                    (i+0.5)*Width, j*Width,
                                    fill="white", width=1)
    elif action == actions[1]:
        return board.create_polygon((i+0.5-triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5+triangle_size)*Width, (j+1-triangle_size)*Width,
                                    (i+0.5)*Width, (j+1)*Width,
                                    fill="white", width=1)
    elif action == actions[2]:
        return board.create_polygon((i+triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    i*Width, (j+0.5)*Width,
                                    fill="white", width=1)
    elif action == actions[3]:
        return board.create_polygon((i+1-triangle_size)*Width, (j+0.5-triangle_size)*Width,
                                    (i+1-triangle_size)*Width, (j+0.5+triangle_size)*Width,
                                    (i+1)*Width, (j+0.5)*Width,
                                    fill="white", width=1)


def render_grid():
    global specials, Width, x, y, player_M
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            for action in actions:
                temp[action] = create_triangle(i, j, action)
            cell_scores[(i,j)] = temp
    for (i, j, c, w, b) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
        board.create_text(i*Width + 50, j*Width + 50, text=b, fill = "black", font=('Helvetica 15 bold'))
    for (i, j, c, w, b) in drop_off:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
        board.create_text(i*Width + 50, j*Width + 50, text=b, fill = "black", font=('Helvetica 15 bold'))
    #for (i, j) in walls:
     #   board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()

def render_count():
    for (i, j, c, w, b) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
        board.create_text(i*Width + 50, j*Width + 50, text=b, fill = "black", font=('Helvetica 15 bold'))
    for (i, j, c, w, b) in drop_off:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
        board.create_text(i*Width + 50, j*Width + 50, text=b, fill = "black", font=('Helvetica 15 bold'))


def set_cell_score(state, action, val):
    global cell_score_min, cell_score_max
    triangle = cell_scores[state][action]
    green_dec = int(min(255, max(0, (val - cell_score_min) * 255.0 / (cell_score_max - cell_score_min))))
    green = hex(green_dec)[2:]
    red = hex(255-green_dec)[2:]
    if len(red) == 1:
        red += "0"
    if len(green) == 1:
        green += "0"
    color = "#" + red + green + "00"
    board.itemconfigure(triangle, fill=color)


def try_move( dx, dy):
    global player_M, x, y, score, walk_reward, me, restart, player_M_block, player_F
    if restart == True:
        restart_game()
    new_x = player_M[0] + dx
    new_y = player_M[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and((new_x, new_y) != player_F) : #and (new_x != player_F[0]) and (new_y != player_F[1]) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player_M = (new_x, new_y)
    for k in range(len(specials)):
        if new_x == specials[k][0] and new_y == specials[k][1]:
            if (player_M_block == False):
                score -= walk_reward
                score += specials[k][3]
                player_M_block = True
                specials[k][4] = specials[k][4] - 1
                print("Picked up block")
    for k in range(len(drop_off)):
        if new_x == drop_off[k][0] and new_y == drop_off[k][1]:
            if (player_M_block == True):
                score -= walk_reward
                score += drop_off[k][3]
                player_M_block = False
                drop_off[k][4] = drop_off[k][4] + 1
                print("Dropped Off")
                #restart = True
                print("score: ", score)
                break

    """ for (i, j, c, w, b) in specials:
        if new_x == i and new_y == j:
            if (player_M_block == False):
                score -= walk_reward
                score += w
                player_M_block = True
                b -= 1
                print("Picked up block")
    for (i, j, c, w, b) in drop_off:
        if new_x == i and new_y == j:
            if (player_M_block == True):
                score -= walk_reward
                score += w
                player_M_block = False
                print("Dropped Off")
                #restart = True
                print("score: ", score)
                return """
    
    #print ("score: ", score)

def try_move_F(dx, dy):
    global player_F, x, y, score, walk_reward, me_F, restart, player_F_block, player_M
    if restart == True:
        restart_game()
    new_x = player_F[0] + dx
    new_y = player_F[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and((new_x, new_y) != player_M) : #and (new_x != player_F[0]) and (new_y != player_F[1]) and not ((new_x, new_y) in walls):
        board.coords(me_F, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player_F = (new_x, new_y)
    for k in range(len(specials)):
        if new_x == specials[k][0] and new_y == specials[k][1]:
            if (player_F_block == False):
                score -= walk_reward
                score += specials[k][3]
                player_F_block = True
                specials[k][4] = specials[k][4] - 1
                print("Picked up block")
    for k in range(len(drop_off)):
        if new_x == drop_off[k][0] and new_y == drop_off[k][1]:
            if (player_F_block == True):
                score -= walk_reward
                score += drop_off[k][3]
                player_F_block = False
                drop_off[k][4] = drop_off[k][4] + 1
                print("Dropped Off")
                #restart = True
                print("score: ", score)
                break


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player_M, score, me, restart
    player_M = (2, y-1)
    player_F = (2,0)
    score = 1
    restart = False
    board.coords(me, player_M[0]*Width+Width*2/10, player_M[1]*Width+Width*2/10, player_M[0]*Width+Width*8/10, player_M[1]*Width+Width*8/10)
    board.coords(me_F, player_F[0]*Width+Width*2/10, player_F[1]*Width+Width*2/10, player_F[0]*Width+Width*8/10, player_F[1]*Width+Width*8/10)


def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player_M[0]*Width+Width*2/10, player_M[1]*Width+Width*2/10,
                            player_M[0]*Width+Width*8/10, player_M[1]*Width+Width*8/10, fill="orange", width=1, tag="me")
me_F = board.create_rectangle(player_F[0]*Width+Width*2/10, player_F[1]*Width+Width*2/10,
                            player_F[0]*Width+Width*8/10, player_F[1]*Width+Width*8/10, fill="blue", width=1, tag="me_F")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
