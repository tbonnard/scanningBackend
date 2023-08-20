from django.db import models
import uuid
import json
# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.title


class Property(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    number = models.CharField(null=False, blank=False, max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class Message(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="propertyMessage")
    description = models.CharField(null=False, blank=False, max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    date_seen = models.DateTimeField(auto_now_add=True)
    probabilityProfanity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    descriptionHighProfanity = models.CharField(null=True, blank=True, max_length=500)
    profanityFlag = models.BooleanField(default=False)
    claimerFlag = models.BooleanField(default=False)

    def __str__(self):
        return self.property + self.description[:11]


class Claim(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="propertyClaimer")
    email = models.EmailField(unique=True, blank=False)
    emailValidated = models.BooleanField(default=False)