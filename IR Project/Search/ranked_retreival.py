# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 12:37:36 2020

@author: NIKHIL
"""
import unidecode
from preprocessing import Preprocess as preprocessing
import queue
import pickle
import math
import bisect

with open('collection.pickle','rb') as f:
    collection = pickle.load(f)
with open('max_tf.pickle','rb') as f:
    max_tf = pickle.load(f)
with open('documentRoot.pickle','rb') as f:
    documentRoot = pickle.load(f)
with open('objs.pickle','rb') as f:
    documentLength,subset , get_index, getReference = pickle.load(f)

while True:
    query = input("Enter a query: ")
    final_query = preprocessing.replace_dates(query)
    final_query = preprocessing.lemma_stop(final_query)
    for i in range(len(final_query)):
        final_query[i] = unidecode.unidecode(final_query[i])
        final_query[i] = final_query[i].lower()
    
    print(final_query)
    
    tf_query = {}
    for w in final_query:
        if w not in tf_query:
            tf_query[w] = 1
        else:
            tf_query[w] += 1
            
    scores = {}
    title_score = {}
    
    N = len(documentRoot)

    wordsInDoc = {}
    
    factor = {}
    
    
    
    for query_term in tf_query:
        
        docs_having_query_term = collection.get_doc_list(query_term, 0)
        df = len(docs_having_query_term)
        idf = 0
        
        if df == 0:
            idf = 0
        else:
            idf = math.log10(N/df)
            
        docs_having_query_term_in_title = collection.get_title_list(query_term,0)
        for docID in docs_having_query_term_in_title:
            if docID in title_score:
                title_score[docID] += idf
            else:
                title_score[docID] = idf
        tfidf_query = tf_query[query_term] * idf
            
        for docID in docs_having_query_term:
            tf_doc = getReference[docID].count_words(query_term, 0)
            tf_doc = 0.5 + 0.5*tf_doc/max_tf[docID]
            tfidf_doc = (tf_doc)
            if docID not in scores:
                scores[docID] = (tfidf_query * tfidf_doc)
                wordsInDoc[docID] = []
                bisect.insort(wordsInDoc[docID], [-tfidf_query * tfidf_doc, query_term])
                factor[docID] = idf
            else:
                scores[docID] += (tfidf_query * tfidf_doc)
                bisect.insort(wordsInDoc[docID], [-tfidf_query * tfidf_doc, query_term])
                factor[docID] += idf
    for docID in scores:
        if documentLength[docID] != 0:
            scores[docID] *= factor[docID]
            if docID in title_score:
                scores[docID] *= 1 + title_score[docID]
    
    
    sorted_scores = sorted(scores.items(), key = lambda kv : kv[1] , reverse = True)
    
    maxshow = min(10, len(scores))
    
    print('============================================')
    
    for i in range(maxshow):
        # print(i)
        print()
        docID = sorted_scores[i][0]
        print('doc ID = ', docID,end='\n')
        cnt = 0
        if sorted_scores[i][0] not in title_score:
            print('title score = ',0)
        else:
            print('title score = ',title_score[sorted_scores[i][0]])
        print()
        print(subset[get_index[docID]][3])
        print()
        count = 0
        found = 0
        words_before=queue.Queue()
        at_start = 1
        display = ""
        for word in subset[get_index[docID]][4].split():
                
            check_with=preprocessing.replace_dates(word)
            check_with = check_with.lower()
            if len(preprocessing.lemma_stop(check_with)) > 0:
                check_with=preprocessing.lemma_stop(check_with)[0]
            else:
                check_with=word
            
            if check_with == wordsInDoc[docID][0][1]:
                found=1
                
            if found == 1:
                display = display + word + " "
                count += 1
                if count == 50:
                    break
            if found == 0:
                words_before.put(word)
                if words_before.qsize()>20:
                    remove=words_before.get()
                    at_start=0
                    
        if not at_start:
            print('...', end = ' ')
        while words_before.qsize() > 0:
            print(words_before.get(), end = ' ')
        print(display, end = ' ')
        print('...', end = ' ')
        print('\n')
        print('tf-idf score=', sorted_scores[i][1])
        print('\n')
        print('============================================')