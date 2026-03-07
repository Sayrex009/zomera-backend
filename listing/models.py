# listing/models.py
from django.db import models
from app.models import User, Category

class announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    area = models.IntegerField()
    rooms = models.IntegerField()
    category = models.ManyToManyField(Category, related_name='announcements') 
    def __str__(self):
        return self.title


class AIGeneration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(announcement, on_delete=models.CASCADE)
    prompt = models.TextField()
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"AI Generation for {self.listing.title} by {self.user.username}"