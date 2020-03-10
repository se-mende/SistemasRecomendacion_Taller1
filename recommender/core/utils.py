import pickle
import os
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from .models import ArtistRating
import numpy as np
import json

module_dir = os.path.dirname(__file__)  # get current directory
cosine_ii_pickle_file_path = os.path.join(module_dir, './predictions/predictions_ii_cosine.p')
pearson_ii_pickle_file_path = os.path.join(module_dir, './predictions/predictions_ii_pearson.p')

cosine_uu_pickle_file_path = os.path.join(module_dir, './predictions/predictions_uu_cosine.p')
pearson_uu_pickle_file_path = os.path.join(module_dir, './predictions/predictions_uu_pearson.p')

cosine_ii_pickle_predictions = pickle.load( open( cosine_ii_pickle_file_path, "rb" ) )
pearson_ii_pickle_predictions = pickle.load( open( pearson_ii_pickle_file_path, "rb" ) )

cosine_uu_pickle_predictions = pickle.load( open( cosine_uu_pickle_file_path, "rb" ) )
pearson_uu_pickle_predictions = pickle.load( open( pearson_uu_pickle_file_path, "rb" ) )

algoCosine_useruser = None
algoPearson_useruser = None
algoCosine_itemitem = None
algoPearson_itemitem = None

def findPredictions(user_id, similarity, model_type):

    pickle_predictions = None
    if similarity == ArtistRating.SimilarityTechnique.COSINE and model_type == ArtistRating.RecommenderModelType.ITEM_ITEM:
        pickle_predictions = cosine_ii_pickle_predictions
    elif similarity == ArtistRating.SimilarityTechnique.COSINE and model_type == ArtistRating.RecommenderModelType.USER_USER:
        pickle_predictions = cosine_uu_pickle_predictions
    elif similarity == ArtistRating.SimilarityTechnique.PEARSON and model_type == ArtistRating.RecommenderModelType.ITEM_ITEM:
        pickle_predictions = pearson_ii_pickle_predictions
    elif similarity == ArtistRating.SimilarityTechnique.PEARSON and model_type == ArtistRating.RecommenderModelType.USER_USER:
        pickle_predictions = pearson_uu_pickle_predictions
    
    if pickle_predictions is None:
        return None

    user_predictions=list(filter(lambda x: x[0]==user_id, pickle_predictions))
    user_predictions.sort(key=lambda x : x.est, reverse=True)
    user_predictions=user_predictions[0:10]

    labels = ['artist', 'estimation']
    df_predictions = pd.DataFrame.from_records(list(map(lambda x: (x.iid, x.est) , user_predictions)), columns=labels)
    
    return json.loads(df_predictions.to_json(orient='records'))

def getTrainSet():
    ratings=pd.read_csv('../Data/preprocessed_user_item_rating.csv', sep = ',', header=0, names = [ 'userid', 'artist-name', 'rating' ] )
    ratings = ratings.loc[:,['userid', 'artist-name','rating']]

    reader = Reader( rating_scale = ( 0, 5 ) )
    #Se crea el dataset a partir del dataframe
    surprise_dataset = Dataset.load_from_df( ratings[ [ 'userid', 'artist-name', 'rating' ] ], reader )
    trainset, testset=  train_test_split(surprise_dataset, test_size=.2)

    return trainset

def findNeighbors(active, similarity, model_type):
    trainset = getTrainSet()

    sim_options = {}
    algo = None
    global algoCosine_itemitem
    global algoCosine_useruser
    global algoPearson_itemitem
    global algoPearson_useruser
    if similarity == ArtistRating.SimilarityTechnique.COSINE and model_type == ArtistRating.RecommenderModelType.ITEM_ITEM:
        sim_options = {'name': 'cosine','user_based': False}
        if algoCosine_itemitem is None:
            algoCosine_itemitem = KNNBasic(k=30, min_k=5, sim_options=sim_options)
            algoCosine_itemitem.fit(trainset)
        algo = algoCosine_itemitem
    elif similarity == ArtistRating.SimilarityTechnique.PEARSON and model_type == ArtistRating.RecommenderModelType.ITEM_ITEM:
        sim_options = {'name': 'pearson_baseline','user_based': False,'shrinkage': 0}
        if algoPearson_itemitem is None:
            algoPearson_itemitem = KNNBasic(sim_options=sim_options)
            algoPearson_itemitem.fit(trainset)
        algo = algoPearson_itemitem
    elif similarity == ArtistRating.SimilarityTechnique.COSINE and model_type == ArtistRating.RecommenderModelType.USER_USER:
        sim_options = {'name': 'cosine','user_based': True}
        if algoCosine_useruser is None:
            algoCosine_useruser = KNNBasic(k=50, min_k=10, sim_options=sim_options)
            algoCosine_useruser.fit(trainset)
        algo = algoCosine_useruser
    elif similarity == ArtistRating.SimilarityTechnique.PEARSON and model_type == ArtistRating.RecommenderModelType.USER_USER:
        sim_options = {'name': 'pearson_baseline','user_based': True,'shrinkage': 0}
        if algoPearson_useruser is None:
            algoPearson_useruser = KNNBasic(sim_options=sim_options)
            algoPearson_useruser.fit(trainset)
        algo = algoPearson_useruser
    
    neighborsList = []
    if model_type == ArtistRating.RecommenderModelType.ITEM_ITEM:
        item_inner_id = algo.trainset.to_inner_iid(active)
        item_neighbors = algo.get_neighbors(item_inner_id, k=5)
        neighbors = (algo.trainset.to_raw_iid(rid) for rid in item_neighbors)
    elif model_type == ArtistRating.RecommenderModelType.USER_USER:
        user_inner_id = algo.trainset.to_inner_uid(active)
        user_neighbors = algo.get_neighbors(user_inner_id, k=5)
        neighbors = (algo.trainset.to_raw_uid(rid) for rid in user_neighbors)
    for neighbor in neighbors:
        neighborsList.append(neighbor)
    
    return neighborsList