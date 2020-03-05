from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from .forms import SearchUserForm

def index(request):

    context = {
        'title': 'Mensaje de contexto'
    }

    return render(request, 'index.html', context=context)

class SearchUserFormView(FormView):
    template_name = 'index.html'
    form_class = SearchUserForm
    success_url = '/results/'
    
    # def get_success_url(self):
    #     return '/'

class UserSearchResultsListView(ListView):
    template_name = 'user_search_results.html'
