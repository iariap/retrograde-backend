from django.db import models
import uuid

# Create your models here.
class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128,null=False, blank=False)
    cards_open = models.BooleanField()
    voting_open = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
