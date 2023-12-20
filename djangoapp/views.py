from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request , id):
    users = User.objects.get(request, id)
    serializer = UserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def updateUser(request,id):
    user = User.objects.get(id=id)
    serializer = UserSerializer(instance=user,data=request.data)

    if serializer.is_valid:
        serializer.save()

    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request,id):
    user = User.objects.get(id=id)
    user.delete()

    return Response("Usuario deletado com sucesso")