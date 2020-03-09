# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:16:06 2020

@author: leidy
"""

import os
import numpy as np
import pandas as pd
from sklearn.metrics import jaccard_score

if not (os.path.exists('C:/Users/leidy/Documents/Septimo/Sistemas de recomendacion/preprocessed_user_item_rating.csv')):
  raise ValueError('El archivo preprocessed_user_item_rating.csv no fue encontrado en el path')
else:
  print("El archivo ha sido cargado")
  
ratings=pd.read_csv('C:/Users/leidy/Documents/Septimo/Sistemas de recomendacion/preprocessed_user_item_rating.csv', sep = ',', header=0, names = [ '', 'userid', 'artist-name', 'count', 'max', 'rating' ] )
ratings = ratings.loc[:,['userid', 'artist-name','rating']]
ratings=ratings.groupby('userid')['artist-name'].apply(lambda x: ','.join(x)).tolist()

#y_true = np.array(ratings)
#y_pred = np.array(ratings[1:len(ratings)])
#y_pred = np.array(ratings[1])
#jaccard_score(y_true)
ListaL=[]
for x in ratings:
    lista=[]
    for y in ratings:
        if x is not y:
            z = len(set(x).intersection(y)) / len(set(x).union(y))
            lista.append(z)
    ListaL.append(lista)
    
pd.DataFrame(ListaL).to_csv('C:/Users/leidy/Documents/Septimo/Sistemas de recomendacion/user-user_jaccard.csv')    
            
        

