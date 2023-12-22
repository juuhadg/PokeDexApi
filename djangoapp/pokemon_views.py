from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Pokemon
from .serializers import PokemonSerializer
from utils import imageUpload
from rest_framework import status
from utils import deleteImage
import json
from django.http import QueryDict
import requests
from io import BytesIO


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
    if 'types' in new_data and ',' in new_data['types']:
        typesArray = new_data['types'].split(',')
        new_data['types'] = typesArray
    

    print(new_data)
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
    

@api_view(['GET'])
def encherPokemons(request):
    for i in range(2, 21):
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}/').text
        json_data = json.loads(response)
        response = json_data
        
        print(response)
        
        url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{response.get("id")}.png'
        imagem = requests.get(url)

        if imagem.status_code == 200:
            form = {}
            form['name'] = response.get('name')
            form['types'] = response.get('types[0].type.name')
            form['height'] = response.get('height')
            form['weight'] = response.get('weight')

            # Configurar o arquivo da imagem corretamente
            form_files = {'image': (f'{response.get("name")}.png', BytesIO(imagem.content))}

            # Enviar a requisição POST com o formulário e o arquivo
            salvarNoBanco = requests.post('http://127.0.0.1:8000/pokemon/create', data=form, files=form_files)
            
            print(salvarNoBanco.text)
        else:
            print('Erro ao baixar a imagem. Código de status:', imagem.status_code)


    return Response(f"sucesso",status=status.HTTP_200_OK)