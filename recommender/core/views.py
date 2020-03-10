from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import SearchUserForm
from django.urls import reverse
from .models import UserProfile, ArtistRating, ArtistActivity
from django.shortcuts import get_object_or_404
import core.utils as utils
from django.core.paginator import Paginator

class HomeView(ListView):
    template_name = 'index.html'
    paginate_by = 40

    def get_queryset(self):
        user_id = self.request.GET.get('user_id')
        if user_id:
            return UserProfile.objects.filter(id__contains=user_id)
        return UserProfile.objects.all()


def user_recommendations(request, user_id):

    model_type = request.GET.get('model_type', ArtistRating.RecommenderModelType.ITEM_ITEM)
    user = get_object_or_404(UserProfile, pk=user_id)

    cosine_neighbors = None
    pearson_neighbors = None

    if model_type == ArtistRating.RecommenderModelType.USER_USER:
        cosine_neighbors = utils.findNeighbors(user.id, ArtistRating.SimilarityTechnique.COSINE,ArtistRating.RecommenderModelType.USER_USER)
        pearson_neighbors = utils.findNeighbors(user.id, ArtistRating.SimilarityTechnique.PEARSON,ArtistRating.RecommenderModelType.USER_USER)

    song_activities = user.artists_activities.order_by('-activity_count')
    song_activities_paginator = Paginator(song_activities, 40)
    page_number = request.GET.get('page', 1)
    song_activities_page = song_activities_paginator.get_page(page_number)

    context = {
        'model_type': model_type,
        'show_action': model_type == ArtistRating.RecommenderModelType.ITEM_ITEM,
        'user': user,
        'artist_activities': song_activities_page,
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
