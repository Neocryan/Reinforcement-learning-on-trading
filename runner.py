import numpy as np
from subprocess import  Popen
def runner():
    try:
        Popen('python viz.py')
        a = 0
        c = 0
        d = np.zeros((50,10))
        while c<3000:
            c+=1
            b = np.random.random(10)
            d[c%50] = b
            with open('log.txt','a') as log:
                log.writelines('{}'.format(list(b)))
            if c > 50:
                with open('log.txt', 'w') as log:
                    s = str(list(list(x) for x in d))[1:-1].replace('], [', ']\n[')
                    log.write(s)
    except KeyboardInterrupt:
        print('Done')

runner()