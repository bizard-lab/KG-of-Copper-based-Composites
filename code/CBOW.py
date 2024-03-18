from torch import  nn
import torch
from torch.nn.functional import cross_entropy,softmax
from utils import  Dataset,process_w2v_data
from visual import show_w2v_word_embedding

corpus=[]
