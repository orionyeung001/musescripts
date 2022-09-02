import xml.etree.ElementTree as ET
import itertools as it
import awkward as ak
import numpy as np
import pickle
import matplotlib.pyplot as plt

run_num = 9695
fstr = f'txt_data/{run_num:05d}.xml'
fstr_np = f'txt_data/{run_num:05d}.npy'
fstr_pkl = f'txt_data/{run_num:05d}.pkl'

delay_bins = (105, 135)
N = 1000

def within(x,b):
    return b[0]<x and x<b[1]


def read_dat():
    # --- loading file from text ---
    print('loading... ',end='', flush=True)
    with open(fstr) as file:
        tree = ET.parse(file)

    print('Done', flush=True)
    dat = tree.getroot()

    return dat

def export_dat(dat):
    print('saving to file... ',end='', flush=True)
    with open(fstr_pkl, 'wb') as f:
        pickle.dump(dat, f)

    with open(fstr_np, 'wb') as f:
        np.save(f, np.array(dat, dtype=object, allow_pickle=True))

    print('Done', flush=True)

def load_dat():

    print('loading pkl... ',end='', flush=True)
    with open(fstr_pkl, 'rb') as f:
        dat=pickle.load(f)

    print('Done', flush=True)

    # print('loading np... ',end='', flush=True)
    # with open(fstr_np, 'rb') as f:
    #     dat = np.load(f)
    # print('Done', flush=True)

    return dat

def parse_trig_hits(hits):
    v = []
    for h in hits:
        if int(h.attrib['id']) == 16:
            s = h.text.replace(' ','')
            v.append(float(s))
    return v

def parse_bh_hits(hits):
    v = []
    for h in hits:
        if int(h.attrib['id'][0]) == 3:
            s = h.text.replace(' ','').split(',')[0]
            v.append(float(s))
    return v



dat = load_dat()
trig_hits = ak.ArrayBuilder()
bh_hits = ak.ArrayBuilder()
good_events = ak.ArrayBuilder()


print('parsing... ',end='', flush=True)
for e in dat:
    trig_hits.begin_list()
    bh_hits.begin_list()
    good_events.begin_list()

    trigs = parse_trig_hits(e[0])
    bhs = parse_bh_hits(e[1])

    for t in trigs:
        trig_hits.real(t)

    for bh in bhs:
        bh_hits.real(bh)

    for (t, bh) in it.product(trigs, bhs):
        if within(t-bh, delay_bins):
            with good_events.list():
                good_events.real(t)
                good_events.real(bh)

    trig_hits.end_list()
    bh_hits.end_list()
    good_events.end_list()

print('Done', flush=True)

trig_hits = trig_hits.snapshot()
bh_hits = bh_hits.snapshot()
good_events = good_events.snapshot()

num_good_p_event = list(map(ak.count, good_events))

plt.figure(1)
bins = [i for i in range(9)]
trig_mult, trig_mult_bins = np.histogram(list(map(ak.count, trig_hits)))
bh_mult, bh_mult_bins = np.histogram(list(map(ak.count, bh_hits)))

plt.step(trig_mult, trig_mult_bins[:-1], label='trig')
plt.step(bh_mult, bh_mult_bins[:-1], label='bh')
plt.title('hit multip')
plt.show()

plt.figure(2)
bins = ak.linspace(-300,100, 401)
trig_times, trig_times_bins = np.histogram(list(it.chain.from_iterable(trig_hits)))
bh_times, bh_times_bins = np.histogram(list(it.chain.from_iterable(bh_hits)))

plt.step(trig_times, trig_times_bins[:-1], label='trig')
plt.step(bh_times, bh_times_bins[:-1], label='bh')
plt.title('hit times')
plt.show()

plt.figure(3)
plt.hist([x[0]-x[1] for x in it.chain.from_iterable(good_events)])
plt.title('good trig-bh')
plt.show()


"""
for ch in e[1]:
    print(ch.tag, ch.attrib, ch.text)
--- event ---
trig_hit {'id': '22'}  -142.6
trig_hit {'id': '16'}  -190.1
trig_hit {'id': '16'}  69.2
BH_hit {'id': '2, 14'}  -295.8, -293.1, 0
BH_hit {'id': '3,  1'}  -290.1, -291.0, 0
--- event ---
trig_hit {'id': '16'}  -212.5
trig_hit {'id': '16'}  -0.1
trig_hit {'id': '16'}  772.6
BH_hit {'id': '2,  8'}  -317.7, -314.9, 0
BH_hit {'id': '3,  4'}  -315.3, -317.4, 0
--- event ---
trig_hit {'id': '22'}  116.1
trig_hit {'id': '16'}  -190.5
trig_hit {'id': '16'}  89.5
BH_hit {'id': '3,  5'}  -290.3, -291.2, 0
BH_hit {'id': '3,  6'}  -292.7, -291.5, 0
BH_hit {'id': '3,  7'}  -292.8, -293.2, 0
BH_hit {'id': '3,  8'}  -292.8, -290.0, 0
--- event ---
trig_hit {'id': '22'}  -147.8
trig_hit {'id': '16'}  -189.7
BH_hit {'id': '2,  9'}  -292.1, -294.3, 0
BH_hit {'id': '3,  7'}  -293.4, -293.6, 0
--- event ---
trig_hit {'id': '16'}  -200.3
BH_hit {'id': '3,  6'}  -301.6, -300.6, 0
"""

