from rest_framework import serializers
from blog.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

