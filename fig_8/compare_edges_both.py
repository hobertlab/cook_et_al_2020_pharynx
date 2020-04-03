#compare edges

import sys
import os
import getopt
import aux
import networkx as nx
import operator


def main(argv):
	#Get input arguments
	try:
		opts, args = getopt.getopt(argv[1:], "ha:b:o:d", 
			["help","","input1=","input2=","output=","directed"]) 
	except getopt.GetoptError:
		print "Warning: Unknown flag!"
		sys.exit(2)
		return 0
	
	A,B,OUTPUT,DIRECTED = None,None,None,False
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print_help("Help/formatWA.h",argv[0])
			return 0
		elif opt in ("-a","--input1"): A = arg
		elif opt in ("-b","--input2"): B = arg
		elif opt in ("-o","--output"): OUTPUT = arg
		elif opt in ("-d","--directed"): DIRECTED = True
	
	A = aux.read_adj(A,DIRECTED)
	B = aux.read_adj(B,DIRECTED)
	
	C = []
	for (e1,e2) in A.edges():
		if B.has_edge(e1,e2):
			C.append([e1,e2,A[e1][e2]['weight'],B[e1][e2]['weight']])

	C.sort(key=operator.itemgetter(2),reverse = True)
	#print Gg['AQR']
	if OUTPUT:
		aux.write_out_list(OUTPUT,C)

		
if __name__ == '__main__':
	main(sys.argv)
