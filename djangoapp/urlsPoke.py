from django.urls import path
from . import pokemon_views

urlpatterns = [
    path('create', pokemon_views.postPokemon),
    path('', pokemon_views.getAllPokemon),
    path('get/<str:id>',pokemon_views.getOnePokemon),
    path('delete/<str:id>',pokemon_views.deletePokemon),
    path('update/<str:id>',pokemon_views.updatePokemon),
    path('encher',pokemon_views.encherPokemons),
    path('uploadImg',pokemon_views.enviarImgEndPoint),
]
