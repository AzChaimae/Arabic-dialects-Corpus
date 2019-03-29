# -*- coding: utf-8 -*-
"""
Created on Sat May 19 11:38:09 2018

@author: Azroumahli Chaimae
"""
# =============================================================================
# Libraries
# =============================================================================
import csv
#import pandas as pd
import regex
from nltk.tokenize import TweetTokenizer 

#import os
#import numpy as np
#import re 
#import codecs
#import sys
#from io import StringIO
# =============================================================================
# reading & layering the tweets 
# The csv file contain a lot f NUll values so we need to use this method
# =============================================================================
with open('arabictweets.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)
# =============================================================================
# the examlpes to try with
# =============================================================================
exe=['1515167758.8095872::@News_Ejazah @KhalidAlmorikhy #خالد_المريخي_يعود_للساحة_بقوة','1515167781.7575412::@7Ahmed7fouad7 يارب ا فؤش..تسلملي والله😍😍❤️']
#backup
exet=['','a','','b','jjhro','','iuo','أجل','ش','أغسطس','ةيءو','أكتوبر','ظبااطأإآةئيصش']
for row in exet:
    savefile=open('exe.csv','a',encoding='utf-8-sig')
    savefile.write(row)
    savefile.write('\n')
    savefile.close()
exen='أ ظبااطأإآةئيصشسذااآآآإأأىئؤةيءوه آ '
exet='b jjhro iuo أجل  ش أغسطس   ةيءو  ظبااطأإآةئيصشسذااآآآإأأىئؤةيءوه  أكتوبر ظبااطأإ آةئيصش'
    
# =============================================================================
# Remove non arabic words (URL + Media)
# =============================================================================

#for exe
exe=[regex.sub('[^\p{Arabic}]',' ',i) for i in exe]
#for file

with open('removedNonArabictweets.csv','r', encoding='utf-8-sig') as RNAT:
    reader=csv.reader(row.replace('\0','') for row in RNAT)
    RNAT=list(reader)

a=len(RNAT)

tweetsnotworkedwith=tweets[a:]


saveFile = open('removedNonArabictweets.csv','a',encoding='utf-8-sig')
for row in tweets:
    for cell in row:
        saveFile.write(regex.sub('[^\p{Arabic}]',' ',cell))
        saveFile.write('\n')
saveFile.close()
            
# =============================================================================
# Remove empty rows function
# =============================================================================

def remove_empty_lines(filename):
    #Overwrite the file, removing empty lines and lines that contain only whitespace.
    with open(filename,encoding='utf-8-sig') as in_file, open(filename,'r+',encoding='utf-8-sig') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()
#for exe
remove_empty_lines('exe.csv')
#for file
remove_empty_lines('removedNonArabictweets.csv')           

# =============================================================================
# Tokenization
# =============================================================================
#for exe
tknzr=TweetTokenizer()
for row in exe:
    i=exe.index(row)
    row=tknzr.tokenize(row) 
    del exe[i]
    exe.insert(i,row)

#for file
#listing the file with only arabic letters
with open('removedNonArabictweets.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

tknzr=TweetTokenizer()
for row in tweets:
    for cell in row:
        with open('tokenizedtweets.csv','a',encoding='utf-8-sig') as savefile:
            wr=csv.writer(savefile,quoting=csv.QUOTE_ALL)
            wr.writerow(tknzr.tokenize(cell))
            savefile.write('\n')

# =============================================================================
# Normalization
# =============================================================================

A='[آ]|[أ]|[إ]'
B='[ؤ]|[ئ]'
C='[ة]'
D='[ي]|[ى]'
r='أ'
u='ء'
v='ه'
w='ي'

def normalizing(string):
        string1=regex.sub('[آ]|[أ]|[إ]',r,string)
        string2=regex.sub('[ؤ]|[ئ]',u,string1)
        string3=regex.sub('[ة]',v,string2)
        string4=regex.sub('[ي]|[ى]',w,string3)
        return string4

#delete empty lines from removedNonArabictweets
remove_empty_lines('removedNonArabictweets.csv')

#overwrite the tweets list by the file that contains only arabic tweets
with open('removedNonArabictweets.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

exen=normalizing(exen)

#for file
saveFile = open('Normalizedtweets.csv','a',encoding='utf-8-sig')
for row in tweets:
    for cell in row:
        saveFile.write(normalizing(cell))
        saveFile.write('\n')
saveFile.close()

remove_empty_lines('Normalizedtweets.csv')

# =============================================================================
# Remove stop words
# =============================================================================

#conevert txt to a csv and list the stop words 
####### I've changed the stopwords file
with open('list.txt','r',encoding='utf-8-sig') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('stopwords.csv','w',encoding='utf-8-sig') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)

#create a list of stopwords
remove_empty_lines('stopwords.csv')
with open('stopwords.csv','r', encoding='utf-8-sig') as SW:
    reader=csv.reader(row.replace('\0','') for row in SW)
    stopwords=list(reader)

stopwordss=[]
i=0
for row in stopwords:
    for cell in row:
        stopwordss.append(" %s " % row[i])

#just to see the words    
for word in stopwordss:
    print (word)

#function to remove stop words
j=0
def remove_stop_words(string):
    for word in stopwordss:
        global j
        string=regex.sub('|'.join([word]),'',string)
        j+=1
    return string
              
#removing stop words from the exe
exet='أجل  ش  جير  أغسطس  ةيءو  ج  ظبااطأإآةئيصش انها ا آآآ إأأى ئؤةي  به   أبدا ظبااطأإ  بَلْهَ  آةئيصش'
exet=remove_stop_words(exet)
print (exet)

#overwrite the list of tweets
with open('Normalizedtweets.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

#from the file
saveFile = open('tweetswithoutstopwords.csv','a',encoding='utf-8-sig')
for row in tweets:
    saveFile.write(remove_stop_words(row[0]))
    saveFile.write('\n')
saveFile.close()

remove_empty_lines('tweetswithoutstopwords.csv')

# =============================================================================
# remove tweets that contains one character or 2 or 3
# =============================================================================

#overwrite the list of tweets
tweets=[]
with open('tweetswithoutstopwords.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

#function to remove the lines from a list
def remove_lines_with_1_2_3(alist):
    for row in alist:
        if len(row)==1 or len(row)==2 or len(row)==3:
            del alist[alist.index(row)]

#remove frow the list tweets
remove_lines_with_1_2_3(tweets)

#create the new file without stopwords or one word tweets
saveFile = open('tweetswithoutstopwords2.csv','a',encoding='utf-8-sig')
for row in tweets:
    for cell in row: 
        saveFile.write(cell)
        saveFile.write('\n')
saveFile.close()

# =============================================================================
# remove retweets and duplicated tweets
# =============================================================================

#overwrite the list of tweets
tweets=[]
with open('tweetswithoutstopwords2.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

#function to remove duplicated data from a list
def remove_duplicated_rows(alist):
    output = []
    seen = set()
    for row in alist:
        if row[0] not in seen:
            output.append(row[0])
            seen.add(row[0])
    return output

#for our list
tweets=remove_duplicated_rows(tweets)

#create the new file without duplicates
saveFile = open('nonduplicatedtweets.csv','a',encoding='utf-8-sig')
for row in tweets:
    saveFile.write(row)
    saveFile.write('\n')
saveFile.close()        

# =============================================================================
# Remove the 'ال' 
# =============================================================================

#overwrite the list of tweets
tweets=[]
with open('nonduplicatedtweets.csv','r', encoding='utf-8-sig') as tweets:
    reader=csv.reader(row.replace('\0','') for row in tweets)
    tweets=list(reader)

#Remove  the 'ال' using the regex fubction

def removing(string):
    string=regex.sub('[ال]','',string)
    return string

for row in tweets:
    saveFile = open('cleantweets.csv','a',encoding='utf-8-sig')
    for cell in row:
        saveFile.write(removing(cell))
        saveFile.write('\n')
    saveFile.close()

remove_empty_lines('cleantweets.csv')

# =============================================================================
# Search special characters & Emoticons
# =============================================================================
   #they are all gone since we used a regex for the tweets
