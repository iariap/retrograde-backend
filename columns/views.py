from cards.views import CardCreationSerializer, CardDetailSerializer
from .models import Column
from boards.models import Board
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, decorators 
from rest_framework.response import Response
from rest_framework import serializers  

class ColumnCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['name', 'data', 'position']


class ColumnDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Column
        fields = ['id','name','created_at','data']

    def get_created_at(self, column):        
        return int(column.created_at.timestamp()) 

class ColumnViewSet(viewsets.ViewSet): 

    def list(self, request):
        columns = Column.objects.all()
        return Response(ColumnDetailSerializer(columns, many=True).data)

    def create(self, request):
        column_data=ColumnCreationSerializer(data=request.data)
        if column_data.is_valid():
            column = ColumnDetailSerializer(column_data.save())
            return Response(column.data, status=201)
        else:
            return Response(column_data.errors, status=500)

    def retrieve(self, request, pk=None):
        board = get_object_or_404(Column, pk=pk)
        data = ColumnDetailSerializer(board)
        return Response(data.data, status=200)

    def update(self, request, pk=None):
        return Response(status=200)

    def partial_update(self, request, pk=None):
        return Response(status=200)

    def destroy(self, request, pk=None):
        return Response(status=200)

    @decorators.action(detail=True, methods=['POST'])
    def cards(self, request, boards_pk=None, pk=None):
        card_data = CardCreationSerializer(request.data)
        column = Column.objects.get(pk=pk)
        board = Board.objects.get(pk=boards_pk)
        card = column.card_set.create(**card_data.data, board=board,owner=request.session['participant'])

        return Response(CardDetailSerializer(card, context={'participant':request.session['participant']}).data,status=201)