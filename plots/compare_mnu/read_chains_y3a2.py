'''A simple python script that reads in omegam and sigma8
and plots using chainconsumer [https://samreay.github.io/ChainConsumer/]
'''

import numpy as np
import os
import sys
from chainconsumer import ChainConsumer
import matplotlib.pyplot as plt
c = ChainConsumer()
names=['$\\Omega_m$','$S_8$']
file = 'chain_2x2pt_wcdm_SR_maglim_NLbias.txt'
f =open(file)
ch=[]
w=[]
for i,line in enumerate(f):
    if line.startswith('#'):
        pass
    else:
        words=line.split()
        om=float(words[0])  # as described in the first line, omegam is the 1st entry on each line
        sigma8=float(words[30]) ## as described on the first line, sigma8 is the 31 entry in each line
        s8=(om/0.3)**.5*sigma8
        ch.append([om,s8])
        w.append(float(words[36]))  #weight, it is column 37
w=np.array(w)
ch=np.array(ch)
f.close()
c.add_chain(ch,parameters=names,weights=w,name=r'\textbf{DES Y3 2x2pt}')
## Then after adding 2 more chains
c.configure(plot_hists=False,sigma2d=False,kde=1.5, colors=["g", "r","b"], linewidths=1.2, legend_kwargs={"loc": "upper right", "fontsize": 10},
            legend_color_text=True, legend_location=(-1, 0),diagonal_tick_labels=False)
fig = c.plotter.plot(legend='t',figsize="column")
fig.savefig('omegams8.png', bbox_inches="tight", dpi=300, transparent=True, pad_inches=0.05)
