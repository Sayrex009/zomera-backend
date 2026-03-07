from django.db import models
from app.models import User

class announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    area = models.IntegerField()
    rooms= models.IntegerField()
    def __str__(self): announcement;

class AIGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    listing = models.ForeignKey(announcement, on_delete=models.CASCADE)

    prompt = models.TextField()

    result = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)