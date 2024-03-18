from node2vec import savemodel
from node2vec import nodemain
from deepwalk import main
from msim import test
# from linemaster import line
from PathSimGNetMine import PathSim
import clustering
import time
s = time.time()

filepath = "dataset/test.txt"

ptmodel = nodemain.model(filepath)  
print(ptmodel.values())


s = time.time()
pathmodel = PathSim.main()
clustering.cluster(list(pathmodel.values()), 'pathsim', 2)
e = time.time()
print("Run time: %f s" % (e - s))