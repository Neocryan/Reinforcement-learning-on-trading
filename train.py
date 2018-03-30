from agent.agent import Agent
from functions import *
import sys
import os
from subprocess import Popen
from collections import deque
dd = 0  # this is for start the plotting shell
try:
    commission_rate = 0.0025
    if len(sys.argv) != 6:
        print "Usage: python train.py [stock] [window] [episodes] [train/test] [draw] "
        exit()

    stock_name, window_size, episode_count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    if sys.argv[4] == 'train':
        train = True
    elif sys.argv[4] == 'test':
        train = False

    draw = True if int(sys.argv[5]) == 1 else False
    start = np.random.randint(1,15000)
    if train:
        agent = Agent(window_size)
    else:
        agent = Agent(50, True, 'model_ep10')
    # data = getStockDataVec(stock_name)
    # data_length = len(data) - 1
    batch_size = 32

    for e in xrange(episode_count + 1):
        if stock_name == 'BTC':
            data = getStockDataVec(stock_name)[start:start+5000]
        else:
            data = getStockDataVec(stock_name)
        data_length = len(data) - 1
        tt = 0
        print "Episode " + str(e) + "/" + str(episode_count)
        state = getState(data, 0, window_size + 1)
        total_profit = 0
        agent.inventory = []
        commission_history = []
        c = []
        total_hist = []
        hold = deque(maxlen=200)
        price = deque(maxlen=200)

        for t in xrange(data_length):

            action = agent.act(state)
            tt += 1
            # sit
            next_state = getState(data, t + 1, window_size + 1)
            reward = 0

            if t == data_length - 1:
                reward += np.sum(data[t] - (np.array(agent.inventory) + np.array(commission_history)))
                total_profit += reward
            if action == 1:  # buy
                agent.inventory.append(data[t])
                if len(agent.inventory) > 1000:
                    reward -= 20

                commission_history.append(data[t] * commission_rate)
                hold.append(len(agent.inventory))
                price.append(data[t])
                try:
                    out = str(list(hold)) + '//' + str(list(price))
                    with open('hold.txt', 'w') as ho:
                        ho.write(str(out))
                except:
                    print('record error on host.txt')
                print "Buy: " + formatPrice(data[t])

            elif action == 2 and len(agent.inventory) > 0:  # sell
                bought_price = agent.inventory.pop(0)
                bought_comm = commission_history.pop(0)
                hold.append(len(agent.inventory))
                price.append(data[t])
                try:
                    out = str(list(hold)) + '//' + str(list(price))
                    with open('hold.txt', 'w') as ho:
                        ho.write(str(out))
                except:
                    print('record error on host.txt')
                print "Buy: " + formatPrice(data[t])
                # reward = max(data[t] - bought_price -bought_comm, 0)
                reward += data[t] - bought_price - bought_comm
                total_profit += data[t] - bought_price - bought_comm
                c.append(data[t] - bought_price - bought_comm)
                total_hist.append(total_profit)
                if draw:
                    if dd == 0:
                        dd += 1
                        Popen('python viz.py', shell=True)

                    if tt % 1 == 0:
                        out = str(list(c)) + '//' +str(list(total_hist))
                        with open('log.txt', 'w') as log:
                            log.write(out)

                print "Sell: " + formatPrice(data[t]) + " | Profit: " + \
                      formatPrice(data[t] - bought_price - bought_comm) + \
                      " | Total Profit: " + formatPrice(total_profit)

            elif action == 0:
                reward -= 1
                hold.append(len(agent.inventory))
                price.append(data[t])
                try:
                    out = str(list(hold)) + '//' + str(list(price))
                    with open('hold.txt', 'w') as ho:
                        ho.write(str(out))
                except:
                    print('record error on host.txt')

            # get total profit at each step.

            done = True if t == data_length - 1 else False

            agent.memory.append((state, action, reward, next_state, done))
            state = next_state

            if done:
                print "--------------------------------"
                print "Total Profit: " + formatPrice(total_profit)
                print "--------------------------------"

            if len(agent.memory) > batch_size:
                agent.expReplay(batch_size)

        if e % 10 == 0:
            agent.model.save("models/model_ep" + str(e))
except KeyboardInterrupt:
    print "--------------------------------"
    print "Total Profit: " + formatPrice(total_profit)
    print "--------------------------------"
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
