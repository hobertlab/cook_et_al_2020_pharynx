#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 Christopher Brittin <cbrittin@aecom.yu.edu>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pymysql as MySQLdb
import Format
import Plots
import matplotlib.pyplot as plt
import matplotlib.axis as AX
from matplotlib.ticker import MultipleLocator
from scipy.stats import ks_2samp

plt.rcParams['lines.linewidth'] = 8
plt.style.use('seaborn-colorblind')




def main():
	Gc = 'Data/pharynx_chem_10_22.csv'
	Gg = 'Data/pharynx_elec.csv'
	Gcsom = 'Data/herm_chem_nature_2019.csv'
	Ggsom = 'Data/herm_elec_nature_2019_2.csv'
	Gg2 = ''
	Gc = Format.Input(Gc).from_CSV_adj()
	Gg = Format.Input(Gg).from_CSV_adj(directed = False)
	Gcsom = Format.Input(Gcsom).from_CSV_adj()
	Ggsom = Format.Input(Ggsom).from_CSV_adj(directed = False)
	w = []
	for (n1,n2) in Gg.edges():
		temp = Gg[n1][n2]['weight']
		w.append(temp)
		if temp > 150: print n1,n2,temp
	print max(w)




	##Gg2 = Format.Input(Gg2).from_CSV_adj(directed = False)
	#Sc = Format.Input([]).get_synapses(Gc,'chemical')
	#Sg = Format.Input([]).get_synapses(Gg,'electrical')
	#Scw = Format.Input([]).get_synapse_weights(Gc,'chemical')
	#Sgw = Format.Input([]).get_synapse_weights(Gg,'electrical')
	#chem_syn_sections = Format.Input([]).get_synapses_sections(Gc,'chemical')
	#gap_syn_sections = Format.Input([]).get_synapses_sections(Gg,'electrical')
	##print len(Sc.edges())
	##print len(Sg.edges())
	#print 'chem',max(chem_syn_sections)
	#print 'gap', max(gap_syn_sections)
	##for (n1,n2) in Sg.edges():
	##	print n1,n2,Sg[n1][n2]['weight']


	
	#Gcout = [Gc.out_degree(n) for n in Gc.nodes()]
	#Gcoutsom = [Gcsom.out_degree(n) for n in Gc.nodes()]
	#print(ks_2samp(Gcout, Gcin))


	
	
##this is where it starts????###
	if True:
		TS = 42
		plt.figure(figsize=(40,40))
		plt.figtext(0.23,0.92,'Chemical synapses',fontsize=85)
		plt.figtext(0.66,0.92,'Gap junctions',fontsize=85)
		#plt.figtext(0.05,0.84,'A',fontsize=32)
		#plt.figtext(0.05,0.70,'B',fontsize=32)
		#plt.figtext(0.05,0.56,'C',fontsize=32)
		#plt.figtext(0.05,0.42,'D',fontsize=32)
		#plt.figtext(0.05,0.29,'E',fontsize=32)
		#plt.figtext(0.05,0.15,'F',fontsize=32)
		#ax = plt.subplot2grid((6,4),(0,0))
		ax = plt.subplot2grid((4,4),(0,0))
		Plots.Network(Gc).degree_distribution('In',Range=(0,21),binSize = 1,yrange=(0,1.05),xlabel='In degree', ylabel = 'Fraction of nodes',normed=True,cumulative=-1,log=False, width = 10.0)
		Plots.Network(Gcsom).degree_distribution('In',Range=(0,44),binSize = 1,yrange=(0,1.05),xlabel='In degree', ylabel = 'Fraction of nodes',normed=True,cumulative=-1,log=False, width = 10.0)
		#ax.set_xscale('log')
		plt.xlim((0,70))
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(0,1))
		ax = plt.subplot2grid((4,4),(0,1))
		Plots.Network(Gc).degree_distribution('Out',Range=(0,11),binSize = 1,yrange=(0,1.05),cumulative=-1,xlabel='Out degree',normed=True,log=False)
		Plots.Network(Gcsom).degree_distribution('Out',Range=(0,63),binSize = 1,yrange=(0,1.05),cumulative=-1,xlabel='Out degree',normed=True,log=False)
		#ax.set_xscale('log')
		plt.xlim((0,70))
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(0,2),colspan=2)
		ax = plt.subplot2grid((4,4),(0,2),colspan=2)
		Plots.Network(Gg).degree_distribution('Undirected',Range=(0,11),binSize = 1,yrange=(0,1.05),cumulative=-1,xlabel='Number of neighbors',normed=True,log=False)
		Plots.Network(Ggsom).degree_distribution('Undirected',Range=(0,57),binSize = 1,yrange=(0,1.05),cumulative=-1,xlabel='Number of neighbors',normed=True,log=False)
		#ax.set_xscale('log')
		plt.xlim((0,70))
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(1,0),colspan = 2)
		#Plots.Network(Scw).presynaptic_distribution(Range=(0,45),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Number of sections',ylabel='Fraction of synapses',normed=True,log=True)
		#ax.set_xscale('log')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(1,2),colspan=2)
		#Plots.Network(Sgw).presynaptic_distribution(Range=(0,45),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Number of sections',normed=True,log=True)
		#ax.set_xscale('log')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(2,0),colspan = 2)
		#Plots.Network(Sc).weight_distribution(Range=(0,70),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Number of synapses',ylabel='Fraction of edges',normed=True,log=True)
		#ax.set_xscale('log')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(2,2),colspan = 2)
		#Plots.Network(Sg).weight_distribution(Range=(0,70),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Number of synapses',normed=True,log=True)
		#ax.set_xscale('log')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(3,0),colspan = 2)
		ax = plt.subplot2grid((4,4),(1,0),colspan = 2)
		Plots.Network(Gc).weight_distribution(Range=(0,72),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Synaptic weights',ylabel='Fraction of edges',normed=True,log=False)
		Plots.Network(Gcsom).weight_distribution(Range=(0,142),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Synaptic weights',ylabel='Fraction of edges',normed=True,log=False)
		#ax.set_xscale('log')
		plt.xlim(0,150)
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(3,2),colspan = 2)
		ax = plt.subplot2grid((4,4),(1,2),colspan = 2)
		Plots.Network(Gg).weight_distribution(Range=(0,9),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Synaptic weights',normed=True,log=False)
		Plots.Network(Ggsom).weight_distribution(Range=(0,81),binSize=1,yrange=(0,1.05),cumulative=-1,xlabel='Synaptic weights',normed=True,log=False)
		#ax.set_xscale('log')
		plt.xlim(0,90)
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(4,0),colspan = 2)
		ax = plt.subplot2grid((4,4),(2,0),colspan = 2)
		#Plots.Network(Gc).node_weight_variance(yrange=(0,100),ylabel='Synaptic weights',xlabel='Nodes ordered by magnitude of spread')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(4,2),colspan = 2)
		
		#Plots.Network(Gg).node_weight_variance(yrange=(0,80),xlabel='Nodes ordered by magnitude of spread')
		#plt.setp(ax.get_xticklabels(),fontsize=TS)
		#plt.setp(ax.get_yticklabels(),fontsize=TS)
		#ax = plt.subplot2grid((6,4),(5,0),colspan = 2)
		#ax = plt.subplot2grid((4,4),(3,0),colspan = 2)
		Plots.Network(Gc).cumulative_load(xlabel='Synaptic weights',ylabel='Cumulative load')
		Plots.Network(Gcsom).cumulative_load(xlabel='Synaptic weights',ylabel='Cumulative load')
		plt.xlim(0,80)
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		minorLocator = MultipleLocator(.2)
		ax.yaxis.set_minor_locator(minorLocator)
		#ax = plt.subplot2grid((6,4),(5,2),colspan = 2)
		#ax = plt.subplot2grid((4,4),(3,2),colspan = 2)
		ax = plt.subplot2grid((4,4),(2,2),colspan = 2)
		Plots.Network(Gg).cumulative_load(xlabel='Edge weights')
		Plots.Network(Ggsom).cumulative_load(xlabel='Edge weights')	
		plt.xlim(0,180)
		plt.setp(ax.get_xticklabels(),fontsize=TS)
		plt.setp(ax.get_yticklabels(),fontsize=TS)
		minorLocator = MultipleLocator(.2)
		ax.yaxis.set_minor_locator(minorLocator)
		plt.savefig('distribution_figure411_new_3.eps')
		plt.show()

	
	
	Format.WriteOut('chemical_map.txt').map_file(Gc,'CHEMICAL')
	Format.WriteOut('gap_map.txt').map_file(Gg,'ELECTRICAL')
	#Format.WriteOut('added_gap_map.txt').map_file(Gg2,'ELECTRICAL')

	return 0

if __name__ == '__main__':
	main()

