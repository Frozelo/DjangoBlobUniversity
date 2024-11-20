from rest_framework import viewsets
from blog.models import Categorie
from .serializers import CategorySerializer


class YourModelViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
