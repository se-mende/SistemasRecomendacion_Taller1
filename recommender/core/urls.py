from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchUserFormView.as_view(), name='index'),
    path('results/', views.UserSearchResultsListView.as_view(), name='search_results')
]