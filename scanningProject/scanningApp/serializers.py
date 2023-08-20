from rest_framework import serializers
from .models import Post, Property, Message, Claim


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = '__all__'
        fields = ['id', 'description','profanityFlag', 'property', 'probabilityProfanity', 'created', 'claimerFlag']


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'
