from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import User
from cards.models import Card
from cards.serializers import CardSerializer
from cards.permissions import UserOnlyPostPermission, CardAccessPermission


class CardList(ListCreateAPIView):
    permission_classes = (IsAuthenticated, UserOnlyPostPermission)
    serializer_class = CardSerializer

    def get_queryset(self):
        if self.request.user.role == User.USER:
            return Card.objects.all().filter(user__id=self.request.user.id)
        else:
            return Card.objects.all().filter(company__id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        new_card = Card()
        new_card.user = request.user
        serializer = CardSerializer(instance=new_card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, CardAccessPermission)
