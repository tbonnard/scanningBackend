import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import Http404

from ..serializers import MessageSerializer
from ..models import Message, Property

from .hateSpeechlViews import validateHateSpeech
from .hateSpeechlViewsSightEngine import  validateHateSpeechSight


class MessagesView(APIView):
    def get(self, request, number):
        queryset = Message.objects.filter(property=Property.objects.filter(number=number).first())
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)


class MessageView(APIView):
    def get(self, request):
        queryset = Message.objects.all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        textToReplace = 'The message has been hidden due to a potentially inappropriate message.'
        if serializer.is_valid(raise_exception=True):
            newMessage = serializer.save()
            hateValidationSight = validateHateSpeechSight(newMessage.description)
            print(hateValidationSight)
            if len(hateValidationSight['profanity']['matches']) > 0:
                newMessage.descriptionHighProfanity = newMessage.description
                newMessage.description = textToReplace
                profanityLevel = hateValidationSight['profanity']['matches'][0]['intensity']
                match profanityLevel:
                    case 'high':
                        newMessage.probabilityProfanity = 100.00
                    case 'medium':
                        newMessage.probabilityProfanity = 75.00
                    case 'low':
                        newMessage.probabilityProfanity = 50.00
                    case default:
                        newMessage.probabilityProfanity = 25.00
                newMessage.profanityFlag = True
                newMessage.save()
            else:
                newMessage.save()
            updatedSerializer = MessageSerializer(newMessage)
            return Response(updatedSerializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# WHEN FUKAI WILL WORK
    def postWHENFUKAIOK(self, request):
        serializer = MessageSerializer(data=request.data)
        textToReplace = 'The message has been hidden due to a potentially inappropriate message.'
        if serializer.is_valid(raise_exception=True):
            newMessage = serializer.save()

            hateValidationFukAi = validateHateSpeech(newMessage.description)
            print(hateValidationFukAi)

            # with fukAI because error server 500 if profanity -- EN only
            if hateValidationFukAi is False:
                newMessage.descriptionHighProfanity = newMessage.description
                newMessage.description = textToReplace
                newMessage.probabilityProfanity = 100.00
                newMessage.profanityFlag = True
                newMessage.save()

            elif hateValidationFukAi:
                hateValidationSight = validateHateSpeechSight(newMessage.description)
                print(hateValidationSight)
                if len(hateValidationSight['profanity']['matches']) > 0:
                    newMessage.descriptionHighProfanity = newMessage.description
                    newMessage.description = textToReplace
                    profanityLevel = hateValidationSight['profanity']['matches'][0]['intensity']
                    match profanityLevel:
                        case 'high':
                            newMessage.probabilityProfanity = 100.00
                        case 'medium':
                            newMessage.probabilityProfanity = 75.00
                        case 'low':
                            newMessage.probabilityProfanity = 50.00
                        case default:
                            newMessage.probabilityProfanity = 25.00
                    newMessage.profanityFlag = True
                    newMessage.save()
                else:
                    newMessage.probabilityProfanity = hateValidationFukAi['result']['probability']
                    newMessage.save()
            updatedSerializer = MessageSerializer(newMessage)
            return Response(updatedSerializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailsView(APIView):
    """
    Retrieve, update or delete an instance.
    """
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = MessageSerializer(instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instance = self.get_object(pk)
        serializer = MessageSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response('Data erased', status=status.HTTP_204_NO_CONTENT)