from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Pokemon
from .serializers import PokemonSerializer
from utils import imageUpload
from rest_framework import status
from utils import deleteImage
import json
from django.http import QueryDict


@api_view(['POST'])
def postPokemon(request):
    if 'image' not in request.FILES:
        return Response("Por favor, passe a Imagem do Pokemon a ser Salvo", status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']
    url = imageUpload.upload_image_to_s3(image_file, 'pokemonbucketjuuh', 'imagens')
    
    if not url:
        return Response("Ocorreu um erro ao fazer upload da Imagem", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    new_data = request.data.copy()
    new_data['image'] = url

    serializer = PokemonSerializer(data=new_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllPokemon(request):
     pokemons = Pokemon.objects.all()
     serializer = PokemonSerializer(pokemons, many=True)
     return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def getOnePokemon(request,id):
    pokemon = Pokemon.objects.get(id=id)
    if not pokemon:
        return Response("Pokemon Nao Foi Encontrado",status=status.HTTP_400_BAD_REQUEST)

    
    serializer = PokemonSerializer(pokemon,many=False)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
def updatePokemon(request,id):
    pokemon = Pokemon.objects.get(id=id)
    if not pokemon:
        return Response("Pokemon Nao Foi Encontrado",status=status.HTTP_400_BAD_REQUEST)
    
    new_data = request.data
    

    if 'image' in request.FILES:
        image_file = request.FILES['image']
        url = imageUpload.upload_image_to_s3(image_file,'pokemonbucketjuuh','imagens')
        if url:
            deleteImage.delete_image_from_s3(pokemon.image,'pokemonbucketjuuh')
            new_data['image'] = url
            

    if 'types' in request.data:
        types = request.data.getlist('types')
        new_data['types'] = types

    for key, value in new_data.items():
        setattr(pokemon, key, value)
   
    pokemon.save()
    return Response('Pokemon Atualizado com Sucesso',status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deletePokemon(request,id):
    pokemon = Pokemon.objects.get(id=id)
    if not pokemon:
        return Response("Pokemon Nao Foi Encontrado",status=status.HTTP_400_BAD_REQUEST)
    pokemon.delete()
    deleteImage.delete_image_from_s3(pokemon.image,'pokemonbucketjuuh')
    return Response(f"Pokemon {pokemon.name} Deletado com sucesso",status=status.HTTP_200_OK)
    
