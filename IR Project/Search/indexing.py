# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:03:49 2020

@author: NIKHIL
"""
import pandas as pd
import numpy as np
from preprocessing import Preprocess as preprocessing
import unidecode
import trie
import pickle 
import math
import queue
import time
from tqdm import tqdm

data = pd.read_csv("reuters.csv")
data = np.array(data)
np.save("datan",data)
data = np.load("datan.npy",allow_pickle = True)

get_docID = {}
get_index = {}


NN = len(data)
for i in range(0, len(data)) :
    get_docID[i] = data[i][0]
    get_index[data[i][0]] = i
    
subset = []
counter = 0
for document in data:
    subset.append(document)
    counter += 1
    if counter == NN:
        break
    


start = time.time()

titles = []
contents = []
for document in tqdm(subset):
    document[4] = preprocessing.remove_htmlcodes(document[4])
    
    modifiedContent = preprocessing.replace_dates(document[4])
    modifiedContent = preprocessing.lemma_stop(preprocessing.clean_document(modifiedContent))
    modifiedTitle = preprocessing.lemma_stop(preprocessing.clean_document(document[2]))
    
    for i in range(len(modifiedContent)):
        modifiedContent[i] = modifiedContent[i].lower()
    
    titles.append(modifiedTitle)
    contents.append(modifiedContent)
    
print(time.time() - start)

contents_temp = contents

titles_temp = titles

for i in range(NN):
    for j in range(len(contents[i])):
        contents[i][j] = unidecode.unidecode(contents[i][j])
    for j in range(len(titles[i])):
        titles[i][j] = unidecode.unidecode(titles[i][j])
        
getReference = {}
documentRoot = []
collection = trie.CollectionNode()

for i in range(NN):
    newDocument = trie.Node()
    documentRoot.append(newDocument)
    getReference[get_docID[i]] = newDocument
max_tf = {}


start = time.time()
for i in tqdm(range(NN)):
    for w in contents_temp[i]:
        collection.add_document(w, 0, get_docID[i])
        documentRoot[i].add(w, 0)
        if get_docID[i] in max_tf:
            max_tf[get_docID[i]] = max(documentRoot[i].count_words(w, 0), max_tf[get_docID[i]])
        else:
            max_tf[get_docID[i]] = documentRoot[i].count_words(w, 0)
    for w in titles_temp[i]:
        collection.add_title(w, 0, get_docID[i])
        
print(time.time() - start)

documentLength = {}
N = len(documentRoot)

for i in tqdm(range(len(documentRoot))):
    
    docID = get_docID[i]
    length = 0
    document = documentRoot[i]
    q = queue.Queue()
    q.put([document, ''])
    
    while q.qsize() > 0:

        current = q.get()
        reference = current[0]
        word = current[1]

        if reference.words > 0:
            df = len(collection.get_doc_list(word, 0))
            idf = math.log10(N/df)
            length += (reference.words * idf) ** 2

        for i in range(256):
            if reference.children.get(i) is not None:
                new_word = word + chr(i)
                q.put([reference.children[i], new_word])
    documentLength[docID] = length**0.5
    
    
    
pickle_out = open("collection.pickle","wb")
pickle.dump(collection,pickle_out)
pickle_out.close()
pickle_out1 = open("documentRoot.pickle","wb")
pickle.dump(getReference,pickle_out1)
pickle_out1.close()
pickle_out2 = open("max_tf.pickle","wb")
pickle.dump(max_tf,pickle_out2)
pickle_out2.close()
with open('objs.pickle', 'wb') as f: 
    pickle.dump([documentLength,subset , get_index, getReference], f)

