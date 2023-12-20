from rest_framework import serializers
from .models import User,Pokemon

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  
class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = '__all__'  