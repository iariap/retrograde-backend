from django.db import models

# Create your models here.
class Column(models.Model):
    name=models.CharField(max_length=128)
    data = models.JSONField(null=True, blank=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey('boards.Board', on_delete=models.CASCADE)