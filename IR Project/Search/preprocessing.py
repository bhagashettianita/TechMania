# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 11:05:16 2020

@author: NIKHIL
"""

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
import wordninja
from datetime import datetime

class Preprocess:
    def remove_htmlcodes(document):
        replacement = {
                        "&ampnbsp": ' ',
                        "&ampamp": '&',
                        "&ampquot": '\'',
                        "&ampldquo": '\"',
                        "&amprdquo": '\"',
                        "&amplsquo": '\'',
                        "&amprsquo": '\'',
                        "&amphellip": '...',
                        "&ampndash": '-',
                        "&ampmdash": '-'
                      }
        for str in replacement:
            document = document.replace(str, replacement[str])
            
        return document
    
    def get_wordnet_pos(word):
        
        tag=nltk.pos_tag([word])[0][1][0].upper()
        tag_dict={"J": wordnet.ADJ, 
                  "N": wordnet.NOUN,
                  "V": wordnet.VERB,
                  "R": wordnet.ADV}
        return tag_dict.get(tag,wordnet.NOUN)
    
    def lemma_stop(string):
        
        lemmatizer = WordNetLemmatizer()
        tokenizer = RegexpTokenizer('\w+|\$]\d\[+|\S+,-')
        tokenized = tokenizer.tokenize(string)
        lemmatized = [lemmatizer.lemmatize(w,Preprocess.get_wordnet_pos(w)) for w in tokenized]
        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in lemmatized if w.lower() not in stop_words]
        return filtered_sentence
    
    def is_not_credible (text):
        
        match = re.search(r'[!@#?&{}()]', text)    
        if match:
            return True
        else:
            return False
        
    def scrub_words (text):
        
        text = re.sub('[!@#?&{}()]', '', text)
        text=re.sub(r'[^\x00-\x7F]'," ",text)
        return text
    
    def clean_document (document_string):    
        
        cleaned_doc = document_string
        for word in document_string.split():
                    if Preprocess.is_not_credible(word):
                        temp= Preprocess.scrub_words(word)
                        split=wordninja.split(temp)
                        if len(split)>7:
                              cleaned_doc = cleaned_doc.replace(word,'')
                        else:
                            replace_with=' '.join(word for word in split)
                            cleaned_doc = cleaned_doc.replace(word, replace_with)
        return cleaned_doc
    
    
    def replace_dates(documentString):
        
        regEx = '(([0-9]+(/|\\.|-)[0-9]+(/|\\.|-)[0-9]+)|([0-9]+(/|\\.|-)[0-9]+))'
        iterator = re.finditer(regEx, documentString)
        listOfDates = [(m.start(0), m.end(0)) for m in iterator]   
        for indices in listOfDates:
            date = documentString[indices[0]:indices[1]]
            tmp = date
            date = date.replace('.', '/')
            date = date.replace('-', '/')
            count = date.count('/')
            newDate = ''
            if count == 2:
                try:
                    newDate = datetime.strptime(date, '%m/%d/%Y').strftime('%d %b %Y')
                except ValueError:
                    newDate = date
            else:
                try:
                    newDate = datetime.strptime(date, '%m/%d').strftime('%d %b')
                except ValueError:
                    newDate = date          
            newDate = newDate.replace(' ', '')
            documentString = documentString.replace(tmp, newDate)    
        return documentString
