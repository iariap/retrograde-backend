from django.db import models

# Create your models here.
class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    who = models.CharField(max_length=127,null=True,blank=True)