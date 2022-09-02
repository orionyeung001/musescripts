"""
Written by Orion Yeung in early June 2022
Used to test plot algorithm used in trigger event display
Abandoned stable: July 4, 2022
"""
import matplotlib.pyplot as plt
from itertools import tee

hits = ( (0,True), (1,False), (3,False), (4,True), (6,True), (7,False),
        (9,True), (10,True), (11,False), (13,False), (15,True), )

def plot_builder(hits, yshift=0.0, tbnds=(-10,10), logic_false = False):
    hits = list(sorted(hits, key=lambda p: p[0]))
    tmin, tmax = tbnds

    x,y = [],[]
    x.append(tmin)
    y.append(logic_false)

    x.append(hits[0][0])
    x.append(hits[0][0])
    y.append(y[-1])
    y.append(not y[-1])

    for h in hits[1:]:
        x.append(x[-1])
        x.append(h[0])
        x.append(h[0])

        y.append(not h[1])
        y.append(not h[1])
        y.append(h[1])

    x.append(x[-1])
    y.append(logic_false)

    x.append(tmax)
    y.append(logic_false)

    # convert to numeric
    y = [.5+yshift if i else yshift for i in y]
    return x,y

if __name__ == '__main__':
    plt.plot(*plot_builder(hits))
    plt.show(block=True)
