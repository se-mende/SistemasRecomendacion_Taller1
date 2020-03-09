from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import SearchUserForm
from django.urls import reverse
from .models import UserProfile, ArtistRating
from django.shortcuts import get_object_or_404
import core.utils as utils

class HomeView(ListView):
    model = UserProfile
    template_name = 'index.html'
    paginate_by = 30


def user_recommendations(request, user_id):

    model_type = request.GET.get('model_type', ArtistRating.RecommenderModelType.ITEM_ITEM)
    user = get_object_or_404(UserProfile, pk=user_id)

    cosine_neighbors = None
    pearson_neighbors = None
    if model_type == ArtistRating.RecommenderModelType.USER_USER:
        cosine_neighbors = utils.findNeighbors(user.id, ArtistRating.SimilarityTechnique.COSINE,ArtistRating.RecommenderModelType.USER_USER)
        pearson_neighbors = utils.findNeighbors(user.id, ArtistRating.SimilarityTechnique.PEARSON,ArtistRating.RecommenderModelType.USER_USER)

    context = {
        'model_type': model_type,
        'show_action': model_type == ArtistRating.RecommenderModelType.ITEM_ITEM,
        'user': user,
        'song_activities': [],
        'jaccard_predictions': [],
        'cosine_neighbors': cosine_neighbors,
        'pearson_neighbors': pearson_neighbors
    }

    pearsons_predictions = utils.findPredictions(user_id, ArtistRating.SimilarityTechnique.PEARSON, model_type)
    if pearsons_predictions is not None:
        context['pearson_predictions'] = pearsons_predictions
    
    cosine_predictions = utils.findPredictions(user_id, ArtistRating.SimilarityTechnique.COSINE, model_type)
    if cosine_predictions is not None:
        context['cosine_predictions'] = cosine_predictions

    print(context)
    return render(request, 'user_recommendations.html', context=context)

def item_neighbors(request, artist_name):

    similarity = request.GET.get('similarity', ArtistRating.SimilarityTechnique.PEARSON)
    neighbors = utils.findNeighbors(artist_name,similarity, ArtistRating.RecommenderModelType.ITEM_ITEM)

    context = {
        'artist_name': artist_name,
        'similarity': similarity,
        'neighbors': neighbors
    }
    return render(request, 'item_neighbors.html', context=context)

# class UserRecommendationsDetailView(DetailView):

#     model = UserProfile

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['song_activities'] = self.object.song_activities.all()
#         return context


# class SearchUserFormView(FormView):
#     template_name = 'index.html'
#     form_class = SearchUserForm
    
#     def get_success_url(self):
#         query = self.request.GET.get('query')
#         return '%s?query=%s' %  (reverse('search_results'), query)

# class UserSearchResultsListView(ListView):
#     template_name = 'user_search_results.html'
