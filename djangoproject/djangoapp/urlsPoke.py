from django.urls import path
from . import pokemon_views

urlpatterns = [
    path('create', pokemon_views.postPokemon),
    path('', pokemon_views.getAllPokemon),
]
