import os

import drawgraph
import readdata

cwd=os.getcwd()
filepath=os.path.join(cwd,'data\\triple_sample1.csv')
print(filepath)
triple_statements=readdata.read_to_triple(filepath)


drawgraph.printGraph(triple_statements)
