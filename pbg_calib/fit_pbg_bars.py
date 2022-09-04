import re
from sys import stderr
from os import listdir
import matplotlib.pyplot as plt
import numpy as np, awkward as ak
import uproot, pandas as pd
from scipy.optimize import minimize
import itertools
from scipy.stats import ks_2samp

"""
TODO:
- [ ] use KDestiamtor to obtain callable for pdf of MC data, f_T(t)
- [ ] write resampler of experiment data
- [ ] write f_{X|T}(x;t;params) = normal.pdf(x | t+mu_p, (t*rel_sigma(t; params))^2 + sig_p^2)
- [ ] write integrator with integrate.quad over t for
      f_{X,T}(x,t;params) = f_{X|T}(x;t;params)*f_T(t) to get f_X(x;params)
- [ ] write callable accepting params that evaluates komologorov test for
      experiment came from f_X(x;params)
- [ ] plot all them distributions (since T,X are in the same space)
- [ ] run minimizer for a single bar, see what happens
- [ ] run minimizer for all bars?
"""


def get_hists_from_cooker():
    output_hists = dict()
    fname = '/Users/orion/muse/rootfiles/run13057_PBG_Detail.root'
    with uproot.open(fname) as f:
        for x,y in itertools.product(range(8), repeat=2):
            try:
                obj_key = f'Individual Bars/x = {x}, y = {y}/QDC e Hits'
                output_hists[(x,y)] = f[obj_key]
            except KeyError:
                print(f'could not find item {obj_key}', file=stderr)
    return output_hists

def hist_distance(params, mc_photon, data_counts, data_edges):
    a,b,c,Ecalib = params
    E = mc_photon/Ecalib

    pedestal = np.random.normal(calib_pedestal, calib_pedestal_sigma,
                                len(mc_photon))

    # sample (E\pm\sigma_E) + pedestal noise
    mc_qdc = np.random.normal(E, E*E_rel_sigma(params, mc_photon)) + pedestal
    # account for qdc saturation
    mc_qdc = np.clip(mc_qdc, 0, 3840)
    mc_counts, _ = np.histogram(mc_qdc, data_edges)
    return ks_2samp(data_counts, mc_counts).pvalue

def E_rel_sigma(params, mc_photon):
    """ this will be provided to the optimizer to find the right values for
    a,b,c = params """
    a,b,c,Ecalib = params
    E = y/Ecalib
    return a / np.sqrt(E*0.001) + b + c / (E*0.001);

def store_data():
    g4_fname = '/Users/orion/muse/midasfiles/g4psi_13057.root:T'
    with uproot.open(g4_fname) as t:
        arr = t.arrays(['CAL_PbG_CopyID', 'CAL_PbG_PhotonY'])

    # df.to_hdf("resources/store.h5", "df", append=True)
    return arr


calib_pedestal = 128.80
calib_pedestal_sigma = 3.275
bar_hists = get_hists_from_cooker()
arr = store_data()
n_hits = ak.num(arr['CAL_PbG_CopyID'])
has_hits = arr[n_hits>0]

print('a,b,c,Ecalib')
for x,y in itertools.product(range(3), repeat=2):
    # get cooker data
    counts, edges = bar_hists[(x,y)].to_numpy()
    edges = edges[1:]
    counts = counts[np.logical_and(400<edges, edges<2000)]
    edges = edges[np.logical_and(400<edges, edges<2000)]

    # prep mc data
    bar = x + 64 - ( (1+y) * 8 );
    mc_photon = ak.flatten(has_hits[has_hits.CAL_PbG_CopyID == bar].CAL_PbG_PhotonY)
    res = minimize(hist_distance, (0.05,0.05, 0.02, 2.4),
           args = (mc_photon, counts, edges),
           method = 'L-BFGS-B',
           bounds = ((0.01, 0.1),(0.01, 0.1),(0.01, 0.04),(1,4)))
    if res.success:
        print(f'{res.x}')
    else:
        print(f'None,None,None,None')


""" aim to find a,b,c,ecalib that maximizes likelihood that the data come
from the same distributions """
""" we can get saturation of photon QDC to 3840 so normalize the region under
that since it'll saturate in simulation but possibly not in the detector is
gain matched incorrectly """
