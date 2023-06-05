from django.urls import path

from movies.api.v1.views import MoviesListApi, MovieDetailApi

urlpatterns = [
    path('movies/', MoviesListApi.as_view()),
    path('movies/<uuid:pk>', MovieDetailApi.as_view()),
]
