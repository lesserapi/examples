from django.urls import path
from . import views



urlpatterns = [
    path(
        route='',
        view=views.IndexView.as_view(),
        name='index',
    ),
    
    path(
        route='user_results',
        view=views.UserResultsView.as_view(),
        name='user_results',
    ),
    
    path(
        route='repo_results',
        view=views.RepoResultsView.as_view(),
        name='repo_results',
    ),
    
    path(
        route='repo_info',
        view=views.CheckRepoInformationView.as_view(),
        name='repo_info',
    ),
    
    path(
        route='404',
        view=views.E404View.as_view(),
        name='404',
    ),
]