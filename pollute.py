#!/usr/bin/env python

import os, sys
import networkx as nx
sys.path.append('../../../')
import Holes  as ho
import pickle as pk
import numpy  as np
import glob	

import matplotlib.pyplot as plt

def ProcessFile(filename):
	print("Processing '%s'" % (filename))

	file_title = os.path.splitext(os.path.basename(filename))[0]

	matrix = np.loadtxt(filename, delimiter=",")
	G      = nx.Graph()
	for i in range(0,matrix.shape[0]):
	  for j in range(i,matrix.shape[1]):
	    G.add_edge(i,j,weight=matrix[i][j])


	#Once the network has been loaded, one needs to produce the filtration of the
	#network.   This can be done in different ways. The simplest is to rank the
	#edges in descending order and use their rank as the indices for the sequence
	#of simplicial complex.    Holes contains a few options for different
	#filtrations (ascending, descending, metrical..).    Below we consider the one
	#with descending weights described in
	#[http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0066506]:
	fil = ho.filtrations.dense_graph_weight_clique_rank_filtration(G,2)

	#Once the filtration has been created, it needs to be saved and passed to
	#jython, so that javaplex can receive the data and process it. This requires
	#calling a subprocess and feeding it the right file.
	clique_dictionary_file = './output/'+file_title+'_filtration.pck'
	pk.dump(fil,open(clique_dictionary_file,'w'))

	hom_dim     = 2 # max homology group calculated
	dataset_tag = 'test_IO2009'
	output_dir  = './output/';

	gen_file = './output/gen/generators_test_'+file_title+'_.pck'
	if not os.path.isfile(gen_file):
		ho.persistent_homology_calculation(clique_dictionary_file, hom_dim, dataset_tag, output_dir, jython_call='C:\\jython2.5.4rc1\\jython.bat', m1=2048, m2=2048)


	gen = pk.load(open(gen_file))

	#The properties of each generator can be listed easily:
	gen[1][0].summary()

	#One can also simply produce the barcodes for the network then: 
	ho.barcode_creator(gen[0])
	plt.title(r'Barcode for $H_0$, '+file_title)
	plt.savefig('Barcode0_2006.png')

	ho.barcode_creator(gen[1])
	plt.title(r'Barcode for $H_1$, '+file_title)
	plt.savefig('Barcode1_2006.png')

	ho.barcode_creator(gen[2])
	plt.title(r'Barcode for $H_2$, '+file_title)
	plt.savefig('Barcode2_2006.png')



if len(sys.argv)!=2:
	print("Syntax: %s <INPUT FILES>" % (sys.argv[0]))
	sys.exit(-1)

for filename in glob.glob(sys.argv[1]):
	print filename
#	ProcessFile(filename)
