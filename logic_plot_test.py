import matplotlib.pyplot as plt

logic_false = False
hits = ( (0,True), (1,False), (3,False), (4,True), (6,True), (7,False),
        (9,True), (10,True), (11,False), (13,False), (15,True), )

x,y = [],[]
x.append(-10)
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

y = [1 if i else 0 for i in y]
plt.plot(x,y)
plt.show(block=True)
