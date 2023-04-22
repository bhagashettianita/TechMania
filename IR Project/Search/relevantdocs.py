# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 16:13:04 2020

@author: NIKHIL
"""

from gensim.models.keyedvectors import KeyedVectors
from DocSim import DocSim
import numpy as np
from nltk.corpus import stopwords
data = np.load('datan.npy', allow_pickle = True)
ids = data[:,:1]

def index_of_array(doc_id):
        temp=np.where(ids==doc_id)
        return data[temp][4]
        

googlenews_model_path = './data/GoogleNews-vectors-negative300.bin'

model = KeyedVectors.load_word2vec_format(googlenews_model_path, binary=True)

ds = DocSim(model,stopwords=set(stopwords.words('english')))
input_id = input("Enter Doc id")
output_id = [item for item in input("Enter the list of Docs : ").split()]
source_doc = index_of_array(input("Enter Doc id"))
target_docs = [index_of_array(item) for item in output_id]

sim_scores = ds.calculate_similarity(source_doc, target_docs)

print(sim_scores)