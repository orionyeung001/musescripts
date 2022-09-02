import matplotlib.pyplot as plt
import numpy as np, uproot
import logging, sys
import os
from root_reader import get_data
import pandas as pd


def plot_dist_from_rates(beam_rates, T=20, kmax=3):
    def pmf(k, lam=1):
        return np.exp(-lam)*lam**k/np.math.factorial(k)

    kk = np.arange(kmax+1) # list of `k` observations

    for beam_rate in beam_rates:
        lam = T*beam_rate
        plt.plot(kk,[pmf(k, lam) for k in kk], 'o--',
                 label=f'rate={beam_rate}MHz, $\lambda={lam}$')

    plt.legend()
    plt.yscale('log')
    plt.show(block=True)

def get_filenames():
    """
    this function is called in main to create an iterable with the list of
    valid filenames the filenames in here are not checked, and `uproot.open` is
    used on them directly, so ensure that this only returns valid filenames by
    filtering names found by `os.listdir`
    """
    data_path = '/Users/orion/muse/rootfiles/'
    def listdir_nohidden(path):
        for f in os.listdir(path):
            if not f.startswith('.'):
                yield f
    def file_filter(fname):
        return ''.join(fname.split('_')[1:]).split('.')[0] == 'Triggertiming'
    return map(lambda fname: data_path + fname,
               filter(file_filter, listdir_nohidden(data_path))
               )

obj_key_pattern = 'repeat multiplicity logic'
title_pattern = 'BHD_PID_e'
def object_filter(f, obj_key):
    """
    defines a filter for the objects found in f the idea is that not every
    object in the file will need to be processed by compute_data
    """
    def check_obj_key(obj_key):
        return obj_key.find(obj_key_pattern) > 0
    def check_htitle(h):
        return h.all_members['fTitle'].find(title_pattern) > 0
    return check_obj_key(obj_key) and check_htitle(f[obj_key])

def compute_data_pair(h):
    """ given the raw hist, it outputs the efficiency ratios """
    h_n = h.to_numpy()
    return (h_n[0][1]/h_n[0][0])
def data_filter(d):
    """ cuts entries that have data I don't want to see """
    return d > 0

def get_title(obj):
    return obj.all_members['fTitle']

def get_all_data_from_files():
    data = dict()
    for fname in get_filenames():
        abbr_fname = fname.split('/')[-1]
        logging.info(f"processing file {abbr_fname}")
        with uproot.open(fname) as f:
            d = get_data(f, compute_data_pair,
                         object_filter, data_filter)
            if d is not None:
                data[abbr_fname] = list(d)
        logging.info(f"done processing file {abbr_fname}")
    return data

def runs_and_rates():
    # in kHz
    return {
            10295: 177.526053,
            11002:1636.061764,
            11853:2540.413072,
            11854:2545.428013,
            11855:2543.536788,
            12143: 100.975588,
            12144: 101.564328,
            12145: 101.074938,
            12146: 101.331974,
            12147: 101.072644,
            12148: 101.2446,
            12149: 101.128743,
            12150: 101.30043,
            12151: 100.574298,
            12152: 101.947786,
            12161: 102.595055,
            12162: 100.477123,
            12163: 100.407668,
            12164: 102.53570,
            12165: 100.635231,
            12166: 102.637289,
            12167: 100.503131,
            12168: 100.842555,
            12169: 100.270203,
            12227: 196.801869,
            13055: 195.051307,
            13060: 133.673344,
            13065:  24.568746,
            13206: 243.872588,
            13207: 243.548125,
            13208: 243.171557,
            13209: 243.2818,
            13210: 243.295876,
            }

def from_rootfiles_to_pandas():
    data = get_all_data_from_files()
    rates = runs_and_rates()


    data_in_pairs = []
    for k,v in data.items():
        run_num = int(k.split('_')[0][-5:])
        for pair in v:
            data_in_pairs.append((run_num, rates[run_num],
                                  get_title(pair[0]), pair[1]))
    data_in_pairs.sort(key=lambda x: x[0])

    return pd.DataFrame(data_in_pairs,
                        columns=('run', 'rate', 'titlestr', 'ratio'))


if __name__ == '__main__':
    first_August_run = 13039
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    # # plot from those beam rates
    # plot_dist_from_rates([1e-3, 1e-1, 1e0], 20)

    df_root = from_rootfiles_to_pandas()
    print(df_root)
    df_rises = df_root.loc[df_root.titlestr.map(lambda s: s.find('rises')) > 0]
    df_falls = df_root.loc[df_root.titlestr.map(lambda s: s.find('falls')) > 0]

    for df,cmap,label in [(df_rises, 'Reds', 'rise'), (df_falls, 'Blues', 'fall')]:
        plt.figure()
        plt.hist2d(df.rate, np.log10(df.ratio), cmap=cmap)

        plt.colorbar()
        plt.ylabel(r'$log_{10}(\lambda)$')
        plt.xlabel('rate (kHz)')
        plt.title(f'Repeat {label} multiplicity rate against beam rate')
        plt.savefig(f'png/{obj_key_pattern}_{title_pattern}_{label}.png', dpi=600)

        plt.figure()
        plt.plot(df.run, np.log10(df.ratio), color='xkcd:blue')
        plt.axvline(x=first_August_run, ls='--', color='xkcd:black', label='August 1st')
        plt.ylabel(r'$log_{10}(\lambda)$')
        plt.xlabel('run num')
        plt.title(f'Repeat {label} multiplicity rate over time')
        plt.legend()

        plt.show()
