from django.http import HttpResponse
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from cards.models import Card, User
from cards.serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CardList(APIView):
    def get(self, request):
        if request.user.role == User.USER:
            cards = Card.objects.all().filter(user__id=request.user.id)
        else:
            cards = Card.objects.all().filter(company__id=request.user.id)
        serializer = CardSerializer(cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role == User.COMPANY:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CardSerializer(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
