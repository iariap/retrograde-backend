from cards.models import Card
from boards.models import Board
from votes.models import Vote
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, decorators, serializers
from rest_framework.response import Response

# Create your views here.

class CardCreationSerializer(serializers.ModelSerializer):
#        data = {"id":"3pZGZd9XdEG27H91RJQf","column":"Y68bPXt2gVw6vmwhsXaw","owner":True,"author":"pepe","text":"card1","created_at":1613545330,"votes":0,"voted":False}
    class Meta:
        model = Card
        fields = ['id','column', 'author', 'text' ]

    def get_created_at(self, card):        
        return card.created_at.timestamp()

class CardDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    voted = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()


    class Meta:
        model = Card
        fields = ['id','column', 'author', 'text', 'created_at', 'votes', 'owner', 'voted' ]

    def get_created_at(self, card):        
        return card.created_at.timestamp()

    def get_owner(self, card):
        return card.owner == self.context['participant']

    def get_voted(self, card):
        return self.context['participant'] in (vote.who for vote in card.votes.all())

    def get_votes(self, card):
        return card.votes.count()


class CardViewSet(viewsets.ViewSet):
    def list(self, request, boards_pk=None):
        board = Board.objects.get(pk=boards_pk)
        cards = Card.objects.filter(board=board)
        return Response(CardDetailSerializer(cards, many=True, context={'participant':request.session['participant']}).data)

    def create(self, request):
        card_data=CardCreationSerializer(data=request.data)
        if card_data.is_valid(raise_exception=True):
            card = CardDetailSerializer(card_data.save(owner=request.session['participant']), context={'participant':request.session['participant']})
            return Response(card.data, status=201)

    def retrieve(self, request, pk=None):
        card = get_object_or_404(Card, pk=pk)
        data = CardDetailSerializer(card, context={'participant':request.session['participant']})
        return Response(data.data, status=200)

    def update(self, request, pk=None):
        return Response(status=200)

    def partial_update(self, request, pk=None, boards_pk=None):
        class InputSerializer(serializers.Serializer):
            text = serializers.CharField()
        
        card_data = InputSerializer(data=request.data)
        if card_data.is_valid(raise_exception=True):
            cards = Card.objects.filter(pk=pk, board__id=boards_pk)
            cards.update(**card_data.validated_data)
            return Response(CardDetailSerializer(cards.first(), context={'participant':request.session['participant']}).data, status=200)

    def destroy(self, request, pk=None, boards_pk=None):
        cards = Card.objects.filter(pk=pk, board__id=boards_pk)
        cards.delete()
        return Response(status=200)

    @decorators.action(detail=True, methods=['PUT','DELETE'])
    def vote(self, request, boards_pk=None, pk=None):
        card = Card.objects.filter(pk=pk, board__id=boards_pk).first()
        who = request.session['participant']
        if request.method == 'PUT':
            card.votes.add(Vote.objects.create(who=who))
        elif request.method == 'DELETE':
            card.votes.filter(who=who).delete()

        return Response(status=201)
