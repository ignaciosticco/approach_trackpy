import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pims
import trackpy as tp
import sys
import math
import pylab


first_frame =  int(sys.argv[1])
last_frame =  int(sys.argv[2])
input_imagenes =  sys.argv[3]


input_imagenes = input_imagenes.split(',')
tfilter = pd.read_csv('data_trajectories.txt',sep=' ')

frames_color = pims.ImageSequence(input_imagenes)

j=0
plt.ion()
for i in range(first_frame,last_frame+1):
     fig,ax = plt.subplots(constrained_layout=True) 
     tp.plot_traj(tfilter.query('frame<={0}'.format(i)),superimpose=frames_color[j])
     #tp.plot_traj(tfilter.query('frame<={0}'.format(i)))
     #ax.xlim(0,352)
     #ax.ylim(0,640)
     ax.axis(xmin=0,xmax=352,ymin=0, ymax=640)
     ax.invert_yaxis()
     fig.savefig('output2/out_{}'.format(i))
     j+=1


