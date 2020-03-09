import pickle
import os
import pandas as pd
from .models import ArtistRating
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