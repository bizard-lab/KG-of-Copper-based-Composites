import networkx as nx
from node2vec import node2vec
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import time
s = time.time()



def read_graph(inputs, weighted, directed):
    # Reads the input network in networkx.
    if weighted:
        G = nx.read_edgelist(inputs, nodetype=int, data=(('weight', float),), create_using=nx.DiGraph())
    else:
        G = nx.read_edgelist(inputs, nodetype=int, create_using=nx.DiGraph())
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = 1
    if not directed:
        G = G.to_undirected()
    return G


def learn_embeddings(walkss):
    # Learn embeddings by optimizing the Skipgram objective using SGD.
    outmodel = {}
    mwalks = [list(map(str, walk)) for walk in walkss]
    modelsx = gensim.models.Word2Vec(mwalks, vector_size=20, window=5, min_count=0, epochs=3)  
    for word in modelsx.wv.index_to_key:  # Word2Vec向量转字典
        outmodel[word] = modelsx.wv[word]

    return outmodel, modelsx


def joindata(vecmodel, lablepath):
    lable = {}
    out = {}
    filelable = open(lablepath, "r")


    for line in filelable:
        items = line.replace(':', ' ').strip().split()  
        lable[items[0]] = items[1:]


    for item in lable:
        for value in lable[item]:
            if item in vecmodel:
                out[value] = vecmodel[item]
    filelable.close()
    return out


def joinmodel(filepath, lablepath, log):
    walk_length = 80  # Length of walk per source.
    num_walks = 10  # Number of walks per source.
    p = 1  # Return hyperparameter.
    q = 1  # Inout hyperparameter.
    weighted = False
    directed = False

    files = filepath
    nx_G = read_graph(files, weighted, directed)
    G = node2vec.Graph(nx_G, directed, p, q)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks, walk_length)  

    ptmodels, YuanModels = learn_embeddings(walks)  
    joinmodels = joindata(ptmodels, lablepath)

    if log == 0:
        return YuanModels 
    if log == 1:
        return ptmodels  
    if log == 2:
        return joinmodels  


def model(filepath):
    walk_length = 80  # Length of walk per source.
    num_walks = 10  # Number of walks per source.
    p = 1  # Return hyperparameter.
    q = 1  # Inout hyperparameter.
    weighted = False
    directed = False
    files = filepath
    nx_G = read_graph(files, weighted, directed)
    G = node2vec.Graph(nx_G, directed, p, q)
    G.preprocess_transition_probs()
    walks = G.simulate_walks(num_walks, walk_length)  
    ptmodels, YuanModels = learn_embeddings(walks) 

    return ptmodels 
e = time.time()

