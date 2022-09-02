import os, sys, re
import logging
import matplotlib.pyplot as plt
import numpy as np, uproot, pandas as pd
import itertools

def compute_data(h):
    """ given the raw hist, it outputs the efficiency ratios """
    h_n = h.to_numpy()
    return (h_n[0][1]/h_n[0][0])

def get_filenames():
    data_path = '/Users/orion/muse/rootfiles/'
    regex = re.compile(r'^run\d{5}_Trigger_timing\.root$')
    return map(lambda fname: data_path + fname,
            filter(regex.match, os.listdir(data_path))
               )

def get_beam_rate(run_num):
    # in kHz
    return {10295: 177.526053, 11002: 1636.061764, 11853: 2540.413072, 11854: 2545.428013, 11855: 2543.536788, 12143: 100.975588, 12144: 101.564328, 12145: 101.074938,
            12146: 101.331974, 12147: 101.072644,  12148: 101.2446,    12149: 101.128743,  12150: 101.30043,   12151: 100.574298, 12152: 101.947786, 12161: 102.595055,
            12162: 100.477123, 12163: 100.407668,  12164: 102.53570,   12165: 100.635231,  12166: 102.637289,  12167: 100.503131, 12168: 100.842555, 12169: 100.270203,
            12227: 196.801869, 13055: 195.051307,  13060: 133.673344,  13065: 24.568746,   13206: 243.872588,  13207: 243.548125, 13208: 243.171557, 13209: 243.2818,
            13210: 243.295876, }[run_num]

def append_values(out_dat, fname, f, obj_key):
    run_num = int(fname.split('_')[0][-5:])
    plot_title = f[obj_key].all_members['fTitle']
    out_dat.loc[len(out_dat.index)] = [
            run_num, # run number
            get_beam_rate(run_num), # metadata
            plot_title, # hist_identifier
            compute_data(f[obj_key]), # data we want
            ]

def find_matching_keys(pattern):
    fnames = list(get_filenames())
    with uproot.open(fnames[0]) as f:
        obj_keys = f.keys(filter_name=pattern)
        obj_keys = list(map(lambda s: s.split(';')[0], obj_keys))
    return obj_keys

def create_matching_keys(*args):
    """ returns '/'.join of each string as outer product from each list
    Useful for traversing cooker output since each item has similar structure
    Example use:
    >> list(create_matching_keys(['a','b'],
                                 ['fancy'],
                                 ['x','yz']))
        ['a/fancy/x', 'b/fancy/x', 'a/fancy/yz', 'b/fancy/yz']
    """
    return ["/".join(p) for p in itertools.product(*args)]

def process():
    # init table of N x 4 with labeled columns, and how to add data to it
    output_data = pd.DataFrame(columns=('run', 'rate', 'titlestr', 'ratio'))

    # get the keys, preferred method is explicit formation of keys
    obj_keys = create_matching_keys(['Ch16 BHD_PID_e', 'Ch17 BHD_PID_pi'],
                                    ['raw timing'],
                                    ('repeat multiplicity logic ' + e for e in ['fall','rise'])
                                    )

    # # can alternatively regex needs to be surrounded by /'s or shell glob match the keys
    # obj_key_pattern = '/^Ch\d{2} BHD_PID_.*repeat multiplicity logic (rise|fall)/'
    # obj_key_pattern = '*BHD_PID_*repeat multiplicity logic*'
    # obj_keys = find_matching_keys(obj_key_pattern)

    for fname in get_filenames():
        abbr_fname = fname.split('/')[-1]
        logging.debug(f'processing {abbr_fname}')

        with uproot.open(fname) as f:
            # iterate over matching hists in each matching file
            for obj_key in obj_keys:
                try:
                    # .append_values() only has to know how to process one histogram
                    # no need to modify anything in these nested for loops
                    append_values(output_data, fname, f, obj_key)
                except KeyError:
                    logging.warning(f'could not find item {obj_key}')

    return output_data

# logging levels are CRITICAL, ERROR, WARNING, INFO, DEBUG, and NOTSET
# we show that level and all higher priority levels
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL) # only shows critical messages

df = process()
df = df.loc[df['ratio'] > 0, df.columns].sort_values(['rate', 'run'])
df['log_ratio'] = df.ratio.map(lambda r: np.log10(r))
df['log_beamrate'] = df.rate.map(lambda r: np.log10(r))
print(df)
df.to_csv('txt/repeat_hit_ratios_df.csv')
df.plot.hexbin(x='log_beamrate', y='log_ratio', gridsize=20)
plt.title('Rate of observed repeat edges of same type')
plt.show()
