from django.db import models
from votes.models import Vote
# Create your models here.
#{
#    "id":"3pZGZd9XdEG27H91RJQf",
#    "column":"Y68bPXt2gVw6vmwhsXaw",
#    "owner":true,
#    "author":"pepe",
#    "text":"card1",
#    "created_at":1613545330,
#    "votes":0,
#    "voted":false
#}

class Card(models.Model):
    author = models.CharField(max_length=128)
    owner = models.CharField(max_length=128, default='')
    text = models.CharField(max_length=2048)
    votes = models.ManyToManyField(Vote)
    created_at = models.DateTimeField(auto_now_add=True)
    column = models.ForeignKey('columns.Column', on_delete=models.CASCADE, default=None)
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE, default=None)
