from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import SearchUserForm
from django.urls import reverse
from .models import UserProfile

# def index(request):

#     context = {
#         'title': 'Mensaje de contexto'
#     }

#     return render(request, 'index.html', context=context)


class HomeView(ListView):
    model = UserProfile
    template_name = 'index.html'
    paginate_by = 30


class UserRecommendationsDetailView(DetailView):

    model = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['song_activities'] = self.object.song_activities.all()
        return context


class SearchUserFormView(FormView):
    template_name = 'index.html'
    form_class = SearchUserForm
    
    def get_success_url(self):
        query = self.request.GET.get('query')
        return '%s?query=%s' %  (reverse('search_results'), query)

class UserSearchResultsListView(ListView):
    template_name = 'user_search_results.html'
