import os, sys, re
import logging
import matplotlib.pyplot as plt
import numpy as np, uproot, pandas as pd, scipy.optimize as optimize
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

def calib_lightoutput_rel_sigma(e, a=0.05, b=0.05, c=0.02, ):
    return a / np.sqrt(e*0.001) + b + c / (e*0.001);

def store_data():
    g4_fname = '/Users/orion/muse/midasfiles/g4psi_13057.root'
    ecalib = 2.4
    with uproot.open(g4_fname) as f:
        t = f['T']
        df = t.arrays(['CAL_PbG_CopyID', 'CAL_PbG_PhotonY'], library='pd')

    df['e'] = df.CAL_PbG_PhotonY.map(lambda y: y/ecalib)
    df.to_hdf("store.h5", "df", append=True)
    return None

# logging levels are CRITICAL, ERROR, WARNING, INFO, DEBUG, and NOTSET
# we show that level and all higher priority levels
logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL) # only shows critical messages

df = pd.read_hdf("store.h5")

""" aim to find a,b,c,ecalib that maximizes likelihood that the data come
from the same distributions """
""" we can get saturation of photon QDC to 3840 so normalize the region under
that since it'll saturate in simulation but possibly not in the detector is
gain matched incorrectly """
