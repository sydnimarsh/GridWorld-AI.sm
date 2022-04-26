__author__ = 'philippe'
import World
import threading
import time
import random

discount = 0.5
actions = World.actions
states = []
Q = {}
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))

for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp

for (i, j, c, w, b) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        World.set_cell_score((i, j), action, w)


def do_action(action):
    s = World.player_M
    r = -World.score
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player_M
    r += World.score
    World.render_count()
    return s, action, r, s2

def do_action_F(action):
    s = World.player_F
    r = -World.score
    if action == actions[0]:
        World.try_move_F(0, -1)
    elif action == actions[1]:
        World.try_move_F(0, 1)
    elif action == actions[2]:
        World.try_move_F(-1, 0)
    elif action == actions[3]:
        World.try_move_F(1, 0)
    else:
        return
    s2 = World.player_F
    r += World.score
    World.render_count()
    return s, action, r, s2

def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val

def P_random_M(s):
    # for all actions check to see if there is an applicable operator to 
    #a drop off or a pick up location
    for action in actions:
        if action == "up":
            new_x = s[0]
            new_y = s[1] - 1
            for (i, j, c, w, b) in World.specials:
                #if pickup has no more blocks do not go
                if (b == 0):
                    continue
                #if in pickup and able to pick up a block do so
                if new_x == i and new_y == j:
                    if (World.player_M_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            #if dropoff is up
            for (i, j, c, w, b) in World.drop_off:
                # if dropoff has max blocks, skip
                if (b == 5):
                    continue
                #if agent has a block, enter into this state
                if new_x == i and new_y == j:
                    if (World.player_M_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "down":
            new_x = s[0]
            new_y = s[1] + 1
            for (i, j, c, w, b) in World.specials:
                if (b == 0):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if (b == 5):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "left":
            new_x = s[0] - 1
            new_y = s[1]
            for (i, j, c, w, b) in World.specials:
                if (b == 0):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if (b == 5):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "right":
            new_x = s[0] + 1
            new_y = s[1]
            for (i, j, c, w, b) in World.specials:
                if b == 0:
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if b == 5:
                    continue
                if new_x == i and new_y == j:
                    if (World.player_M_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
    #if there are no possible operators to a pickup/dropoff location
    #select a random point
    possible = True
    contains = False
    #ensures that the randomly selected point will not enter a dropoff/pickup location
    
    while(possible):
        random_act = random.randint(0,3)
        action = actions[random_act]
        if action == "up":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0]
                new_y = s[1] - 1
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0]
                new_y = s[1] - 1
                if new_x == i and new_y == j:
                    contains = True
        elif action == "down":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0]
                new_y = s[1] + 1
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0]
                new_y = s[1] + 1
                if new_x == i and new_y == j:
                    contains = True
        elif action == "left":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0] - 1
                new_y = s[1] 
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0] - 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
        elif action == "right":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0] + 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0] + 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
        if contains:
            contains = False
            continue
        else:
            possible = False 
    for a,q in Q[s].items():
        if a == action:
            val = q
    return action, val

def P_random_F(s):
    # for all actions check to see if there is an applicable operator to 
    #a drop off or a pick up location
    print(s[0], s[1])
    for action in actions:
        if action == "up":
            new_x = s[0]
            new_y = s[1] - 1
            for (i, j, c, w, b) in World.specials:
                #if pickup has no more blocks do not go
                if (b == 0):
                    continue
                #if in pickup and able to pick up a block do so
                if new_x == i and new_y == j:
                    if (World.player_F_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            #if dropoff is up
            for (i, j, c, w, b) in World.drop_off:
                # if dropoff has max blocks, skip
                if (b == 5):
                    continue
                #if agent has a block, enter into this state
                if new_x == i and new_y == j:
                    if (World.player_F_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "down":
            new_x = s[0]
            new_y = s[1] + 1
            for (i, j, c, w, b) in World.specials:
                if (b == 0):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if (b == 5):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "left":
            new_x = s[0] - 1
            new_y = s[1]
            for (i, j, c, w, b) in World.specials:
                if (b == 0):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if (b == 5):
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
        elif action == "right":
            new_x = s[0] + 1
            new_y = s[1]
            for (i, j, c, w, b) in World.specials:
                if b == 0:
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == False):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
            for (i, j, c, w, b) in World.drop_off:
                if b == 5:
                    continue
                if new_x == i and new_y == j:
                    if (World.player_F_block == True):
                        for a,q in Q[s].items():
                            if a == action:
                                val = q
                        return action, val
    #if there are no possible operators to a pickup/dropoff location
    #select a random point
    possible = True
    contains = False
    #ensures that the randomly selected point will not enter a dropoff/pickup location
    
    while(possible):
        random_act = random.randint(0,3)
        action = actions[random_act]
        if action == "up":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0]
                new_y = s[1] - 1
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0]
                new_y = s[1] - 1
                if new_x == i and new_y == j:
                    contains = True
        elif action == "down":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0]
                new_y = s[1] + 1
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0]
                new_y = s[1] + 1
                if new_x == i and new_y == j:
                    contains = True
        elif action == "left":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0] - 1
                new_y = s[1] 
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0] - 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
        elif action == "right":
            for (i,j,c,w,b) in World.specials:
                new_x = s[0] + 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
            for (i,j,c,w,b) in World.drop_off:
                new_x = s[0] + 1
                new_y = s[1]
                if new_x == i and new_y == j:
                    contains = True
        if contains:
            contains = False
            continue
        else:
            possible = False 
    for a,q in Q[s].items():
        if a == action:
            val = q
    return action, val



def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    time.sleep(1)
    alpha = .3
    t = 1
    change = True
    while True:

        # Pick the right action
        if change == False:
            s = World.player_M
            #max_act, max_val = max_Q(s)
            max_act, max_val = P_random_M(s)
            print(max_act, max_val)
            (s, a, r, s2) = do_action(max_act)

            # Update Q
            max_act, max_val = max_Q(s2)
            inc_Q(s, a, alpha, r + discount * max_val)
        else:
            s = World.player_F
            #max_act, max_val = max_Q(s)
            max_act, max_val = P_random_F(s)
            print(max_act, max_val)
            (s, a, r, s2) = do_action_F(max_act)

            # Update Q
            max_act, max_val = max_Q(s2)
            inc_Q(s, a, alpha, r + discount * max_val)

        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(.1)
            t = 1.0
        #print(Q[s])
        if change:
            change = False
        else:
            change = True

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
