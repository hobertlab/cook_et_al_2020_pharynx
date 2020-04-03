#compare_core.py

import aux
import networkx as nx
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt


def cumulative_load(G1,G2,title,label,ylabel):		
	def get_XY(G):
		weights = []
		for (n1,n2) in G.edges(): weights.append(G[n1][n2]['weight'])
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

	
	
		return X,Y,imin
	
	X1,Y1,imin1 = get_XY(G1)
	X2,Y2,imin2 = get_XY(G2)
	
	
	
	plt.plot(X1,Y1,lw=3,color='r')
	plt.plot(X2,Y2,lw=3,color='b')

	
	
	plt.legend(('All %s edges' %label,'Unique %s edges' %label),loc='lower right')	
	plt.ylim(0,1.02)
	plt.xlim(0,60)
	plt.xlabel('Edge weight, w',fontsize=24)
	if ylabel: plt.ylabel('Fraction of edges < w',fontsize=24)
	plt.title(title,fontsize=24)
	#if 'xlabel' in kwargs: plt.xlabel(kwargs['xlabel'],fontsize = FS)
	#if 'ylabel' in kwargs: plt.ylabel(kwargs['ylabel'],fontsize = FS)
	#if 'title' in kwargs: plt.title(kwargs['title'], fontsize = 36)	
		

	
		
def main():
	#Synaptic edges
	Na = aux.read_adj('Data/n2w_roi_chem2.csv',True)
	Ja = aux.read_adj('Data/jsa_chem2.csv',True)

	#Neighbor edges
	#Nn = aux.read_adj('Data/n2u_neighbors_nr.txt',False)
	#Jn = aux.read_adj('Data/jsh_neigh_all.txt',False)
	
	if True:
		rmfile = 'muscles.txt'
		Na = aux.remove_nodes(rmfile,Na)
		Ja = aux.remove_nodes(rmfile,Ja)
		#Nn = aux.remove_nodes(rmfile,Nn)
		#Jn = aux.remove_nodes(rmfile,Jn)

	if False:
		#Adjust neighbors
		for (e1,e2) in Na.edges():
			Nn.add_edge(e1,e2,weight=Na[e1][e2]['weight'])
			
		for (e1,e2) in Ja.edges():
			Jn.add_edge(e1,e2,weight=Ja[e1][e2]['weight'])

	#Na = aux.convert_to_frac_out(Na)
	#Ja = aux.convert_to_frac_out(Ja)	
	
	#Syn edge differential
	synNa_not_Ja = list(set(Na.edges())-set(Ja.edges()))
	synJa_not_Na = list(set(Ja.edges())-set(Na.edges()))	

	N_all,J_all = nx.DiGraph(Na),nx.DiGraph(Ja)
	N_unique,J_unique = nx.DiGraph(),nx.DiGraph()
	
	for (e1,e2) in synNa_not_Ja: N_unique.add_edge(e1,e2,weight=N_all[e1][e2]['weight'])
	for (e1,e2) in synJa_not_Na: J_unique.add_edge(e1,e2,weight=J_all[e1][e2]['weight'])
	
	plt.figure()
	plt.subplot(121)
	cumulative_load(N_all,N_unique,'N2W','N2W',True)
	plt.subplot(122)
	cumulative_load(J_all,J_unique,'JSA','JSA',False)
	plt.show()
	
	for (e1,e2) in synNa_not_Ja: Na.remove_edge(e1,e2)
	for (e1,e2) in synJa_not_Na: Ja.remove_edge(e1,e2)	
	
	for n in set(Na.nodes()) - set(Ja.nodes()):Na.remove_node(n)
	for n in set(Ja.nodes()) - set(Na.nodes()):Ja.remove_node(n)
	
	#Na = aux.convert_to_frac_out(Na)
	#Ja = aux.convert_to_frac_out(Ja)
	
	D = nx.DiGraph()
	for (e1,e2) in Na.edges():
		D.add_edge(e1,e2,weight = Na[e1][e2]['weight'] - Ja[e1][e2]['weight'])
	
	#print D['RMGR']
	w = [ [e1,e2,D[e1][e2]['weight']] for (e1,e2) in D.edges()]
	ss = sorted(w,key = itemgetter(2))
	#for s in sorted(w,key = itemgetter(2)):
	#	print s[0],s[1],s[2]		
	#aux.write_out_list('core_frac_diff.csv',ss)

if __name__ == '__main__':
	main()
