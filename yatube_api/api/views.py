from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer, CatListSerializer

# Create your views here.
