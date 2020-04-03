import csv
import networkx as nx
import re

def get_args(kwargs,default):
	#kwargs: keyword arguments
	#default: dictionary of default values
	args = {}
	for d in default:
		if d in kwargs:
			args[d] = (kwargs[d])
		else:
			args[d] = (default[d])
	return args

def read_csv_data(fin,**kwargs):
	#kwargs:
	#	header: number of lines in the header, if not defined, header is assumed to be 0
	#	delimiter: string used as delimiter, if not defined, delimiter is assumed to be ','	
	fIn = open(fin, 'rb')
	lst = []
	delimiter = ','
	if 'header' in kwargs:
		i = 0
		while i <= kwargs['header']: 
			fIn.next()
			i += 1
	if 'delimiter' in kwargs: delimiter = kwargs['delimiter']
	fInReader = csv.reader(
		fIn,delimiter = delimiter, quotechar = ' ', quoting = csv.QUOTE_ALL)
	for line in fInReader:
		lst.append(line)
	fIn.close()
	return lst

def remove_nodes(fin,G):
	#Removes nodes and associated inputs from graph G
	#Get nodes to be removed
	REMOVE = get_list_from_file(fin)
	REMOVE = set(REMOVE) & set(G.nodes())
	#Remove nodes from graph
	for r in REMOVE:
		G.remove_node(r)
	return G

def group_nodes(fIn,G):
	#Group nodes and associated outputs from graph G.  
	#Returns the H, the resulting graph
	
	#Get node groupings
	GROUPS = get_groups(fIn)
	#Group nodes
	if nx.is_directed(G):
		H = nx.DiGraph()
	else:
		H = nx.Graph()
	
	for e in G.edges():
		attr = G[e[0]][e[1]]
		if e[0] in GROUPS:
			n1 = GROUPS[e[0]]
		else:
			n1 = e[0]
		if e[1] in GROUPS:
			n2 = GROUPS[e[1]]
		else:
			n2 = e[1]
		if (n1,n2) in H.edges():
			#print n1,n2,H[n1][n2]
			H[n1][n2]['weight'] += attr['weight']
			H[n1][n2]['loc'].extend(attr['loc'])
			H[n1][n2]['sections'].extend(attr['sections'])
			H[n1][n2]['contin'].extend(attr['contin']) 
		else:
			H.add_edge(n1,n2,weight = attr['weight'],loc=attr['loc'],contin=attr['contin'],sections=attr['sections'])
	
	return H

def keep_nodes(fIn,G):
	KEEP = get_list_from_file(fIn)
	return G.subgraph(KEEP)

def get_groups(fIn):
	fIn = open(fIn,'rb')
	fInReader = csv.reader(
		fIn,delimiter = ',', quotechar = ' ', quoting = csv.QUOTE_NONE)
	grps = {}
	for line in fInReader:
		idx = line.index('-->')
		tKey = line[0:idx]
		tMap = line[idx+1]
		for i in range(len(tKey)):
			grps[tKey[i]]=tMap
	fIn.close()
	return grps

def get_list_from_file(fin):
	fIn = open(fin,'rb')
	fInReader = csv.reader(
		fIn,delimiter = ',', quotechar = ' ', quoting = csv.QUOTE_NONE)	
	lst = [l[0] for l in fInReader]
	fIn.close()
	return lst

def write_adj(fOut,G):
	fOut = open(fOut,'wb')
	
	fOut.write('*Nodes %d\n' %nx.number_of_nodes(G))
	for n in sorted(G.nodes()):
		line = ''.join([n,'\n'])
		fOut.write(line)
	
	fOut.write('*Edges %d\n' %nx.number_of_edges(G))
	for (n1,n2) in G.edges():
		line = ','.join([n1,n2,str(G[n1][n2]['weight'])])
		line = ''.join([line,'\n'])
		fOut.write(line)
	
	fOut.close()

def read_adj(fIn,directed,**kwargs):	
	min_weight = 0
	if 'min_weight' in kwargs: min_weight = int(kwargs['min_weight'])
	if directed:
		G = nx.DiGraph()
	else:
		G = nx.Graph()	
	print fIn
	fIn = open(fIn,'rb')
	fIn.next() #skip first line
	fInReader = csv.reader(
		fIn,delimiter = ',', quotechar = ' ', quoting = csv.QUOTE_NONE)
	
	read_nodes = True
	
	for line in fInReader:			
		if "Edges" in line[0]:
			read_nodes = False 
		elif read_nodes:
			G.add_node(line[0])
		else:
			if float(line[2]) > min_weight:	G.add_edge(line[0],line[1],weight=float(line[2]))	
	fIn.close()

	return G

def write_json(fOut,Gc,Gg):
	import json
	data = format_json(Gc,'chem') + format_json(Gg,'gap')
	fOut = open(fOut,'w')
	print >> fOut,json.dumps(data)
	fOut.close()
	
def format_json(G,syn_type):
	data = []
	for (n1,n2) in G.edges():
		data.append({'source':n1,'target':n2,'type':syn_type,'weight':G[n1][n2]['weight']})
	return data

def rm_brack(s):
	return re.sub('[\[\]]','',s)

def write_syn(fOut,G):
	fOut = open(fOut,'w')
	
	fOut.write('Node1,Node2,sect1,sect2\n')
	
	for (n1,n2) in sorted(G.edges()):
		loc = G[n1][n2]['loc']
		cont = map(str,G[n1][n2]['contin'])
		sections = map(str,G[n1][n2]['sections'])
		for i in range(len(loc)):
			l = loc[i].split('-')
			line = ','.join([n1,n2,l[0],l[1],cont[i],sections[i]])
			line = ''.join([line,'\n'])
			fOut.write(line)
	
	fOut.close()

def read_syn(fIn,directed):
	if directed:
		G = nx.DiGraph()
	else:
		G = nx.Graph()	
	fIn = open(fIn,'r')
	fIn.next() #skip first line
	fInReader = csv.reader(
		fIn,delimiter = ',', quotechar = ' ', quoting = csv.QUOTE_NONE)
		
	for (n1,n2,s1,s2,cont,sect) in fInReader:
	#for (n1,n2,s1,s2,cont) in fInReader:
		if '#' not in n1:
			if not directed: 
				[n1,n2] = sorted([n1,n2])
				if ((n1,n2) not in G.edges()) and ((n2,n1) not in G.edges()): G.add_edge(n1,n2,weight=0,loc=[],contin=[],sections=[])
			else:
				if (n1,n2) not in G.edges(): G.add_edge(n1,n2,weight=0,loc=[],contin=[],sections=[])
			#G[n1][n2]['weight'] += abs(int(s1)-int(s2)+1)
			G[n1][n2]['weight'] += int(sect)
			G[n1][n2]['loc'].append('-'.join([s1,s2]))
			G[n1][n2]['contin'].append(cont)
			G[n1][n2]['sections'].append(int(sect))
			
	return G	
		
def read_into_list(fIn):
	fIn = open(fIn,'r')
	fInReader = csv.reader(
		fIn,delimiter = ',', quotechar = ' ', quoting = csv.QUOTE_NONE)	
	return [row for row in fInReader if '#' not in row[0] ]
		
def filter_und_list(X):
	X2 = []
	for x in X:
		if x[1] == '' and [x[2],x[1],x[0],x[3],x[4],x[5],x[6]] not in X2:
			X2.append(x)
		if x[2] == '' and [x[1],x[0],x[2],x[3],x[4],x[5],x[6]] not in X2:
			X2.append(x)
	return X2

def switch_LR(G):
	def switch(s,cnew,idx):
		snew = list(s)
		snew[idx] = cnew
		return ''.join(snew)
	
	new,lr = {},{}		
	for n in G.nodes():
		if n[-1] == 'L':
			temp = switch(n,'R',-1)
			temp2 = n[:-1]
		elif n[-1] == 'R':
			temp = switch(n,'L',-1)
			temp2 = n[:-1]
		else:
			temp = n
			temp2 = n
		if temp in G.nodes(): 
			new[n] = temp
			lr[n] = temp2
		else:
			new[n] = n
			lr[n] = n
				
	if nx.is_directed(G): 
		H = nx.DiGraph()
	else:
		H = nx.Graph()  
	
	for (a,b) in G.edges():
		H.add_edge(new[a],new[b])
		H[new[a]][new[b]] = G[a][b]
		if not nx.is_directed(G):
			H[new[b]][new[a]] = G[a][b]
	
	return H,lr

def filter_floor(G,floor):
	for (a,b) in G.edges():
		print a,b,G[a][b]['weight']
		if G[a][b]['weight'] < floor: G.remove_edge(a,b)
	nodes = G.nodes()
	for n in nodes:
		if not G.degree(n): G.remove_node(n)	
	return G

def filter_ceil(G,ceil):
	for (a,b) in G.edges():
		if G[a][b]['weight'] > ceil: G.remove_edge(a,b)
	nodes = G.nodes()
	for n in nodes:
		if not G.degree(n): G.remove_node(n)	
	return G

def in_strength(G,node):
	#Networkx does not compute weighted in degree correctly
	s = 0.0
	for k in G.predecessors(node):
		s += G[k][node]['weight']
	return s

def pajek(G,fOut):
	print 'Writing Pajek file: %s' %fOut
	nodes = {}
	nodes2 = []; i = 0
	for n in sorted(G.nodes()):
		i += 1
		nodes[n] = i
		nodes2.append((str(i),''.join(['"',n,'"']))) 
	
	edges = []
	for e in G.edges():
		n1 = nodes[e[0]]
		n2 = nodes[e[1]]
		w = float(G[e[0]][e[1]]['weight'])
		edges.append((str(n1),str(n2),str(w)))
	
	num_nodes = len(nodes)
	num_edges = len(edges)
	
	fOut = open(fOut,'wb')
	
	fOut.write('*Vertices %d\n' %num_nodes)
	for n in nodes2:
		line = ' '.join([n[0],n[1]])
		line = ''.join([line,'\n'])
		fOut.write(line)
	
	fOut.write('*Arcs %d\n' %num_edges)
	for e in edges:
		line = ' '.join([e[0],e[1],e[2]])
		line = ''.join([line,'\n'])
		fOut.write(line)
	
	fOut.close()

def infomap_results(fIn,fOut):
	fIn = open(fIn,'rb')
	fOut = open(fOut, 'wb')
	fInReader = csv.reader(
		fIn,delimiter = ' ', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
	fInReader.next()
	modules = {}
	for line in fInReader:
		[m,rank] = line[0].split(':')
		m = int(m)
		if m not in modules: modules[m] = []
		modules[m].append(line[2])
	for m in modules:
		fOut.write("\n\nComminity %d\n" %m)
		fOut.write("-----------------------------------\n")
		fOut.write(','.join(modules[m]))
		fOut.write("\n\n")
		fOut.write(','.join(sorted(modules[m])))
		
	fIn.close()
	fOut.close()

def infomap_module_dict(G,fIn):
	fIn = open(fIn,'rb')
	fInReader = csv.reader(
		fIn,delimiter = ' ', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
	fInReader.next()
	modules = {}
	for line in fInReader:
		[m,rank] = line[0].split(':')
		modules[line[2]] = int(m)
	
	mmax = max(modules.values())
	mlast = mmax + 1
	for n in set(G.nodes()) - set(modules.keys()):
		modules[n] = mlast
	
	fIn.close()
	return modules	
	
def write_out_dict(fOut,Dic,**kwargs):
	if 'order' in kwargs: order = kwargs['order']
	else: order = 0
	print fOut
	fOut = open(fOut,'wb')
	fWriter = csv.writer(fOut,delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
	if order == 1:
		for key,value in sorted(Dic.iteritems(), key = lambda (k,v): (v,k)): 
			fWriter.writerow([key,value])
	elif order == 0:
		for d in Dic: fWriter.writerow([d,Dic[d]])
	elif order == -1:
		for key,value in sorted(Dic.iteritems(), key = lambda (k,v): (v,k),reverse=True): fWriter.writerow([key,value])
	fOut.close()	
	
def write_matlab_csv(fOut,G,**kwargs):
	nodes = None
	args = get_args(kwargs,{'order':None,'delimiter':','})	
	if args['order']:
		#nodes = get_dict_from_file(args['order'],args['delimiter'])
		#nodes = get_node_order(nodes)
		#nodes.extend(sorted(set(G.nodes())-set(nodes)))
		#nodes = get_list_from_file(args['order'])
		nodes = map(str,args['order'])
	fOut = open(fOut,'wb')
	if not nodes: nodes = sorted(G.nodes())
	l1 = ','.join(nodes)
	l1 = ''.join([' ,',l1,'\n'])
	fOut.write(l1)
	for n1 in nodes:
		l = [n1]
		for n2 in nodes:
			if G.has_edge(n1,n2):
				l.append(str(G[n1][n2]['weight']))
			else:
				l.append('')
		l = ','.join(l)
		l = ''.join([l,'\n'])
		fOut.write(l)
	
	fOut.close()

def combine_dir_and_und(G,D):
	def add_edge(n1,n2,G,D):
		if D.has_edge(n1,n2):
			D[n1][n2]['weight'] += 0.5*G[n1][n2]['weight']	
		else:
			D.add_edge(n1,n2,weight=0.5*G[n1][n2]['weight'])
		return D
		
	for (n1,n2) in G.edges():
		D = add_edge(n1,n2,G,D)
		D = add_edge(n2,n1,G,D)
	
	return D	 

def get_node_order(ndict):
	d = dict([(i,[]) for i in set(ndict.values())])
	for n in ndict: d[ndict[n]].append(n)
	return [ n for i in sorted(d.keys()) for n in sorted(d[i])] 	
		
		
def get_dict_from_file(fIn,delimiter):
		fIn = open(fIn,'rb')
		fInReader = csv.reader(
			fIn,delimiter = delimiter, quotechar = ' ', quoting = csv.QUOTE_NONE)
		d = {}
		for line in fInReader:
			d[line[0]] = line[1]
		fIn.close()
		return d

def write_out_list(fOut,List):
	fOut = open(fOut,'wb')
	fWriter = csv.writer(fOut,delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
	for l in List:
		fWriter.writerow(l)
		#fOut.write(''.join([l,'\n']))
	fOut.close()

def write_out_dict(fOut,Dic,**kwargs):
	if 'order' in kwargs: order = kwargs['order']
	else: order = 0
	fOut = open(fOut,'wb')
	fWriter = csv.writer(fOut,delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
	if order == 1:
		for key,value in sorted(Dic.iteritems(), key = lambda (k,v): (v,k)): fWriter.writerow([key,value])
	elif order == 0:
		for d in Dic: fWriter.writerow([d,Dic[d]])
	elif order == -1:
		for key,value in sorted(Dic.iteritems(), key = lambda (k,v): (v,k),reverse=True): fWriter.writerow([key,value])
	fOut.close()		

def convert_to_frac_out(G):
	for n in G.nodes():
		wsum = 0
		for n2 in G.neighbors(n): wsum += G[n][n2]['weight']
		for n2 in G.neighbors(n): G[n][n2]['weight'] /= float(wsum)
		
	return G
	

def filter_graph_weights(G,wmin):
	if nx.is_directed(G):
		H = nx.DiGraph()
	else:
		H = nx.Graph()
	
	H.add_nodes_from(G.nodes())
	for (e1,e2) in G.edges():
		if G[e1][e2]['weight'] >= wmin:
			H.add_edge(e1,e2,weight = G[e1][e2]['weight'])
	return H
		
	

	
