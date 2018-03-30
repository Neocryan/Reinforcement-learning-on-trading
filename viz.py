import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(121)
ax1 = fig.add_subplot(122)
ax2 = ax1.twinx()
ax_hist = ax.twinx()

def ani(i):
    try:
        graph_data = open('log.txt', 'r').read().split('//')
        reward = graph_data[0]
        totalhist = eval(graph_data[1])
        data2 = open('hold.txt', 'r').read().split('//')
        hold = data2[0]
        price = data2[1]
        x = eval(reward)
        y = eval(hold)
        z = eval(price)
        ax1.clear()
        ax_hist.clear()
        ax.clear()
        ax1.bar([i for i in range(len(y))], y, alpha = 0.5)
        ax1.set_ylabel('hold')
        ax.set_ylabel('reward at each time (red)')
        ax.plot(x,c = 'red', label = 'current reward',alpha = 0.7)
        ax_hist.plot(totalhist,c = 'black',label = 'total reward',alpha = 0.5)
        # ax.legend()
        # ax_hist.legend()
        ax_hist.set_ylabel('total rewards (black)')
        ax2.clear()
        ax2.plot(z,c = 'blue')
        # if np.mean(z) < 2000:
        #     ax2.set_ylim((900,3000 ))
        # elif np.mean(z) < 3000:
        #     ax2.set_ylim((2500,4500 ))
        # elif np.mean(z) < 5000:
        #     ax2.set_ylim((4500,6500 ))
        # elif np.mean(z) < 7000:
        #     ax2.set_ylim((6500,8500 ))
        # elif np.mean(z) < 9000:
        #     ax2.set_ylim((8500,10500 ))
        # elif np.mean(z) < 11000:
        #     ax2.set_ylim((10500,12500 ))


        ax2.set_ylabel('price')

    except:
        pass


anii = animation.FuncAnimation(fig, ani, interval=500)
plt.tight_layout()

plt.show()
