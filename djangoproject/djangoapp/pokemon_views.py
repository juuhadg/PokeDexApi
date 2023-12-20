from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Pokemon
from .serializers import PokemonSerializer
from utils import imageUpload
from rest_framework import status


@api_view(['POST'])
def postPokemon(request):
    if 'image' not in request.FILES:
        return Response("Por favor, passe a Imagem do Pokemon a ser Salvo", status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']
    url = imageUpload.upload_image_to_s3(image_file, 'pokemonbucketjuuh', 'imagens')
    
    if not url:
        return Response("Erro ao Enviar sua Imagem", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Crie um novo dicionário de dados para incluir a URL da imagem
    new_data = request.data.copy()
    new_data['image'] = url

    serializer = PokemonSerializer(data=new_data)
    if serializer.is_valid():
        # Salva o objeto Pokemon
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getAllPokemon(request):
     pokemons = Pokemon.objects.all()
     serializer = PokemonSerializer(pokemons, many=True)
     return Response(serializer.data,status=status.HTTP_200_OK)