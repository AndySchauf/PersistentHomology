#!/usr/bin/env python

import os, sys
import networkx as nx
sys.path.append('../../../')
import Holes  as ho
import pickle as pk
import numpy  as np

import matplotlib.pyplot as plt

gen_file = './output/gen/generators_test_IO2007_.pck'
if not os.path.isfile(gen_file):
	os.environ["JAVA_OPTS"]="-Xms2048m -Xmx2048m"
	ho.persistent_homology_calculation(clique_dictionary_file, hom_dim, dataset_tag, output_dir, jython_call='C:\\jython2.5.4rc1\\jython.bat', m1=2048, m2=2048)


gen = pk.load(open(gen_file))

#The properties of each generator can be listed easily:
gen[1][0].summary()

#One can also simply produce the barcodes for the network then: 
ho.barcode_creator(gen[0])
plt.title(r'Barcode for $H_0$, IO2007')
plt.savefig('Barcode0.png')

ho.barcode_creator(gen[1])
plt.title(r'Barcode for $H_1$, IO2007')
plt.savefig('Barcode1.png')

ho.barcode_creator(gen[2])
plt.title(r'Barcode for $H_2$, IO2007')
plt.savefig('Barcode2.png')