import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(121)
ax1 = fig.add_subplot(122)


def ani(i):
    try:
        graph_data = open('log.txt', 'r').read().split('//')
        reward = graph_data[0]
        hold = open('hold.txt', 'r').read()
        x = eval(reward)
        y = eval(hold)
        ax1.clear()
        ax.clear()
        ax1.bar([i for i in range(len(y))], y)
        ax1.set_title('hold')
        ax.set_title('reward at each time')
        ax.plot(x)
    except:
        pass


anii = animation.FuncAnimation(fig, ani, interval=500)
plt.show()
