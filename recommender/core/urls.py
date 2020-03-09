from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('recomendations/<user_id>/', views.user_recommendations, name='user_recommendations')
]