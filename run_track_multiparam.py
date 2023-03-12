import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pims
import trackpy as tp
import sys
import random

@pims.pipeline
def gray(image):
    return image[:, :, 1]  # Take just the green channel



def crea_agentes(particle_size_min,particle_size_max,min_max_disp,max_max_disp,
	min_memory,max_memory,N_agents):
	'''
	Crea la poblacion inicial de agentes
	Cada agente es un vector de parametros
	'''
	initial_population = []
	
	for i in range(0,N_agents):
		particle_size =  random.randrange(particle_size_min, particle_size_max+1,2) 
		max_disp = random.randrange(min_max_disp,max_max_disp)
		memory = random.randrange(min_memory,max_memory)

		initial_population+=[[particle_size,max_disp,memory]]
	
	return initial_population


######### PARAMETROS ############## 
output_name ='data_trajectories' # Nombre del archivo de salida
particle_size_min = 3
particle_size_max = 10
min_max_disp = 1
max_max_disp = 10
min_memory = 1
max_memory = 100
N_agents = 20
n_chicas = 10 #	 tamano <= de las trayectorias mas chicas a filtrar
###################################

list_max_msd = []
list_mean_msd = []
list_median_msd = []

initial_population = crea_agentes(particle_size_min,particle_size_max,min_max_disp,max_max_disp,
	min_memory,max_memory,N_agents)

with open("{}.txt".format(output_name), "a") as f:
	f.write("particle_size\tmax_disp\tmemory\tcantidad\tmean_l\tmedian_l\tmean_msd\tmedian_msd\n")

for agente in initial_population:

	particle_size = agente[0]	# size de las particulas (en pixels). Debe ser numero impar.  
	max_disp = agente[1]
	memory = agente[2] 		# Cantidad de frames de memoria

	frames = gray(pims.open('input_test/*.png'))
	f = tp.batch(frames[:],diameter=particle_size)
	f = f.drop(['mass','size','ecc','signal','raw_mass','ep'], axis=1)
	t = tp.link_df(f, max_disp, memory=memory)

	#filtro posicion en y
	t = t[t['y']>200]   

	## Quito las trayectorias mas cortas
	tfilter = tp.filter_stubs(t, n_chichas)

	data_msd = tfilter.groupby(['particle']).apply(lambda x: (((x['x']-x['x'].iloc[0])**2+(x['y']-x['y'].iloc[0])**2).sum()/len(x['x']))).reset_index()
	data_length = tfilter.groupby(['particle']).apply(lambda x: len(x['x'])).reset_index()

	######## Analisis ########

	cantidad = int(len(data_length[0]))

	mean_l = round(np.mean(data_length[0]),1)
	median_l = round(np.median(data_length[0]),1)
	#max_l = round(np.max(data_length[0]),1)

	mean_msd = round(np.mean(data_msd[0]),1)
	median_msd = round(np.median(data_msd[0]),1)
	#max_msd = round(np.max(data_msd[0]),1)
	
	######## Output ########
	with open("{}.txt".format(output_name), "a") as f:
		f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(particle_size,max_disp,memory,cantidad,mean_l,median_l,mean_msd,median_msd))

f.close()