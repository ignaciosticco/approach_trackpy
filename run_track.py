import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pims
import trackpy as tp
import sys

@pims.pipeline
def gray(image):
    return image[:, :, 1]  # Take just the green channel

######### PARAMETROS ############## 
output_name ='detect' # Nombre de las imagenes del trackeo
particle_size = 11	# size de las particulas (en pixels). Debe ser numero impar.  
n_long = 10  		# Largo minimo de la trayectoria
n_long_msd = 200 	# Cantidad de trayectorias que sobreviven al filtro del msd
max_disp = 15
memory = 5 		# Cantidad de frames de memoria
#minmass = 1         # Parametro que filtra features (objetos detectados)
#threshold = 0.001    # Parametro que filtra features
###################################


frames = gray(pims.open('input/*.png'))
f = tp.batch(frames[:],diameter=particle_size)
f = f.drop(['mass','size','ecc','signal','raw_mass','ep'], axis=1)
t = tp.link_df(f, max_disp, memory=memory)

#filtro posicion en y
t = t[t['y']>200]   

## Filtro las trayectorias mas largas
#most_frequent = t['particle'].value_counts()[:n_long].index.tolist()
#tfilter = t[t['particle'].isin(most_frequent)]

## Filtro las trayectorias con mayor msd
data_msd = t.groupby(['particle']).apply(lambda x: (((x['x']-x['x'].iloc[0])**2+(x['y']-x['y'].iloc[0])**2).sum()/len(x['x']))).reset_index()
largest_msd = data_msd.nlargest(n_long_msd, 0)['particle'].tolist()
tfilter2 = t[t['particle'].isin(largest_msd)]

## imprimo el dataframe filtrado 
tfilter2.to_csv('data_trajectories.txt',sep=' ',index=False)
#t.to_csv('data_trajectories.txt',sep=' ',index=False)

## Corro la rutina para hacer el video
input_imagenes = ["input/%03d.png" % i for i in range(1,491)] 
lista = np.arange(1,490,5).astype(int) 

for i in lista:
	list_tmp = ",".join(x for x in input_imagenes[i:i+5]) 
	os.system('python3 plot_tracking_trajectories.py {} {} {}'.format(i,i+5,list_tmp))
