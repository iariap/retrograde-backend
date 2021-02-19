from cards.models import Card
from cards.views import CardCreationSerializer, CardDetailSerializer
from .models import Board
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import viewsets, decorators 
from rest_framework.response import Response
from rest_framework import serializers  
import csv

class BoardCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['name', 'data', 'cards_open', 'voting_open']


class BoardDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id','name','cards_open','voting_open', 'created_at', 'data']

    def get_created_at(self, board):        
        return board.created_at.timestamp() 

class BoardViewSet(viewsets.ViewSet):
    # def get 

    def list(self, request):
        boards = Board.objects.filter(owner=request.session['participant'])
        return Response(BoardDetailSerializer(boards, many=True).data)

    def create(self, request):
        board_data=BoardCreationSerializer(data=request.data)
        if board_data.is_valid():
            board = BoardDetailSerializer(board_data.save(owner=request.session['participant']))
            return Response(board.data, status=201)
        else:
            return Response(board_data.errors, status=500)

    def retrieve(self, request, pk=None):
        board = get_object_or_404(Board, pk=pk)
        data = BoardDetailSerializer(board)
        return Response(data.data, status=200)

    def update(self, request, pk=None):
        return Response(status=200)

    def partial_update(self, request, pk=None):
        return Response(status=200)

    def destroy(self, request, pk=None):
        return Response(status=200)

    @decorators.action(detail=True, methods=['POST', 'GET'])
    def columns(self, request, pk=None):
        from columns.views import ColumnCreationSerializer, ColumnDetailSerializer
        board = Board.objects.get(pk=pk)
        if request.method == 'GET':
            columns = board.column_set.all()
            return Response(ColumnDetailSerializer(columns, many=True).data)
        else:
            # es post!
            column_data = ColumnCreationSerializer(request.data)
            column = board.column_set.create(**column_data.data)
            return Response(ColumnDetailSerializer(column).data, status=201)

    @decorators.action(detail=True)
    def csv(self, request, pk=None):
        board = Board.objects.get(pk=pk)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{board.name}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Board', 'Column', 'Text', 'Created by','Votes','Created'])
        for card in board.card_set.all():
            writer.writerow([card.board.name, card.column.name, card.text, card.author or 'Anonymous',card.votes.count(),card.created_at])

        return response
