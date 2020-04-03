#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       Plots.py
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

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D   
from matplotlib.axes import Axes

global FS
FS = 42
plt.rcParams['lines.linewidth'] = 8


class Network:
	def __init__(self,G):
		self.G = G
	
	def degree_distribution(self,degType,**kwargs):
		weighted = False
		if 'weighted' in kwargs: weighted = kwargs['weighted']
		if degType in ['Out','out','OUT']:
			deg = [self.G.out_degree(n) for n in self.G.nodes()]
			#while 0 in deg: deg.remove(0) 
			xlabel = 'Out degree'
		if degType in ['In', 'in', 'IN']:
			deg = [self.G.in_degree(n) for n in self.G.nodes()]
			#while 0 in deg: deg.remove(0)
			xlabel = 'In degree'
		if degType in ['Undirected','undirected','UNDIRECTED']:
			deg = [self.G.degree(n) for n in self.G.nodes()]
			#while 0 in deg: deg.remove(0)
			xlabel = 'Degree'
		
		if 'Range' in kwargs: Range = kwargs['Range']
		else: Range = None
		if 'binSize' in kwargs and Range: bins = float(Range[-1])/kwargs['binSize']
		else: bins = max(deg)
		if 'cumulative' in kwargs: cumulative = kwargs['cumulative']
		else: cumulative = False
		if 'normed' in kwargs: normed = kwargs['normed']
		else: normed = False
		if cumulative: histtype = 'step'
		else: histtype = 'bar'
		if 'log' in kwargs: LOG = kwargs['log']
		else: LOG = False
								
		n,bins,patches = plt.hist(deg,bins = bins,range=Range,normed=normed,cumulative=cumulative,histtype=histtype,log=LOG,lw=15)
		
		if 'yrange' in kwargs: (y1,y2) = kwargs['yrange']
		else: (y1,y2) = (0,max(n))
		plt.ylim(y1,y2)
		if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
		if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'], fontsize = FS)
		if 'title' in kwargs: plt.title(kwargs['title'], fontsize = 36)
				
	
	def presynaptic_distribution(self,w,**kwargs):
		#w = []
		#for i in self.G:
			#for j in self.G[i]:
				#w.extend(self.G[i][j])
		print max(w),len(w),1.0/len(w)
		if 'Range' in kwargs: Range = kwargs['Range']
		else: Range = None
		if 'binSize' in kwargs and Range: bins = float(Range[-1])/kwargs['binSize']
		else: bins = max(w)
		if 'cumulative' in kwargs: cumulative = kwargs['cumulative']
		else: cumulative = False		
		if 'normed' in kwargs: normed = kwargs['normed']
		else: normed = False
		if cumulative: histtype = 'step'
		else: histtype = 'bar'
		if 'log' in kwargs: LOG = kwargs['log']
		else: LOG = False
						
		n,bins,patches = plt.hist(w,bins = bins,range=Range,normed=normed,cumulative=cumulative,histtype=histtype,log=LOG,lw=10)
		#n,bins,patches = plt.hist(w,bins = bins,range=Range,normed=normed,cumulative=cumulative)
		
		if 'yrange' in kwargs: (y1,y2) = kwargs['yrange']
		else: (y1,y2) = (0,max(n))
		plt.ylim(y1,y2)
		if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
		if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'],fontsize = FS)
		if 'title' in kwargs: plt.title(kwargs['title'],fontsize = 36)

	def node_weight_variance(self,**kwargs):
		nrange = {}
		nweights = {}
		for n1 in self.G.nodes():
			N2 = list(self.G.neighbors(n1))
			weights = []
			if N2:
				for n2 in N2: weights.append(self.G[n1][n2]['weight'])
				print(weights)
				wr = max(weights) - min(weights)
				nrange[n1] = wr
				nweights[n1] = weights
				
		sNodes = sorted(nrange.iteritems(),key=lambda(k,v):(v,k),reverse=True)
		i = 0
		data = []
		for (n,r) in sNodes:
			i += 1
			data.append(nweights[n])
		
		plt.boxplot(data,bootstrap=1000)
		plt.setp(plt.gca(), 'xticklabels', [])
		
		if 'yrange' in kwargs: (y1,y2) = kwargs['yrange']
		else: (y1,y2) = (0,max(n))
		plt.ylim(y1,y2)
		if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
		if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'],fontsize = FS)
		if 'title' in kwargs: plt.title(kwargs['title'],fontsize = 36)
						
		
	def weight_distribution(self,**kwargs):
		w = []
		for (n1,n2) in self.G.edges():
			w.append(self.G[n1][n2]['weight'])
		print max(w)		
		if 'Range' in kwargs: Range = kwargs['Range']
		else: Range = None
		if 'binSize' in kwargs and Range: bins = float(Range[-1])/kwargs['binSize']
		else: bins = max(w)
		if 'cumulative' in kwargs: cumulative = kwargs['cumulative']
		else: cumulative = False
		if cumulative: histtype = 'step'
		else: histtype = 'bar'
		if 'normed' in kwargs: normed = kwargs['normed']
		else: normed = False
		if 'log' in kwargs: LOG = kwargs['log']
		else: LOG = False
		
		n,bins,patches = plt.hist(w,bins = bins,range=Range,normed=normed,cumulative=cumulative,histtype=histtype,log=LOG,lw=15)
		
		if 'yrange' in kwargs: (y1,y2) = kwargs['yrange']
		else: (y1,y2) = (0,max(n))
		plt.ylim(y1,y2)
		if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
		if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'],fontsize = FS)
		if 'title' in kwargs: plt.title(kwargs['title'], fontsize = 36)	

					

	def cumulative_load(self,**kwargs):		
		weights = []
		for (n1,n2) in self.G.edges(): weights.append(self.G[n1][n2]['weight'])
		W = np.sum(weights)
		
		w_count = {}
		for w in weights:
			if w not in w_count: w_count[w] = 0
			w_count[w] += 1
		
		X = sorted(w_count)
		Y = []
		for x in X:
			Y.append(float(w_count[x]*x)/W)
		Y = np.cumsum(Y)
		Yt = np.where(Y<0.5,1,Y)
		imin = np.argmin(Yt)
		#plt.axhline(y=Y[imin],xmin=0,xmax=float(X[imin])/X[-1],lw=15)
		#plt.axvline(x=X[imin],ymin=0,ymax=Y[imin],c='darkorange',lw=15)
		
		#plt.text(80,0.5,'50%% of load < %d' %X[imin],fontsize=FS)
		
		plt.plot(X,Y,lw=15)
			
		plt.ylim(0,1.05)
		plt.xlim(0,max(X)+5)
		if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
		if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'],fontsize = FS)
		if 'title' in kwargs: plt.title(kwargs['title'], fontsize = 36)	
		print(Y)

class Plots:
	def __init__(self,data):
		self.data = data
	
	def histogram(self,**kwargs):
		plt.hist(self.data)
		
		


def main():
	
	return 0

if __name__ == '__main__':
	main()

