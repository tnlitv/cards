from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404

from cards.models import Card
from cards.serializers import CardSerializer, UserSerializer
from .permissions import *


class CardList(APIView):
    permission_classes = (IsAuthenticated, UserOnlyPostPermission)

    def get(self, request):
        if request.user.role == User.USER:
            cards = Card.objects.all().filter(user__id=request.user.id)
        else:
            cards = Card.objects.all().filter(company__id=request.user.id)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CardSerializer(
            data=request.data,
            context={
                'method': request.method,
                'user': request.user
            })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, CardAccessPermission)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CardSerializer(
            instance,
            data=request.data,
            partial=partial,
            context={
                'method': request.method,
                'user': request.user
            })
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
