from django.shortcuts import render
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
import requests


from scanningProject.scanningApp.serializers import PostSerializer
from scanningProject.scanningApp.models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        imageToTextDetails = imageToTextApiLayer(request.data['image'])
        return Response(imageToTextDetails, status=status.HTTP_201_CREATED)

        # posts_serializer = PostSerializer(data=request.data)
        # if posts_serializer.is_valid():
        #     image = posts_serializer.save()
        #     imageToTextDetails = imageToTextApiLayer(image.image)
        #     print(imageToTextDetails)
        #     return Response(imageToTextDetails, status=status.HTTP_201_CREATED)
        # else:
        #     print('error', posts_serializer.errors)
        #     return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create your views here.
def testbackend(request, *args, **kwargs):
    # print(request.data)
    imageToTextDetails = imageToTextApiLayer(request.data['image'])
    return Response(imageToTextDetails, status=status.HTTP_201_CREATED)


def get_csrf_token(request):
    csrftoken = get_token(request)
    # print(csrftoken)
    return JsonResponse({'csrftoken': csrftoken})


def uploadimage(request):
    if request.method == 'POST':
        try:
            # print(0)
            # print(request)
            upload = request.FILES['uploadImage']
            # print(1)
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            file_to_text = imageToTextApiLayer(file_url)
            return JsonResponse({'message': 'received from POST', 'file_to_text':file_to_text }, status=200)
        except:
            return JsonResponse({'message':'error'},status=401)
    return JsonResponse({'message': 'received from GET'}, status=200)



def imageToTextApiLayer(filename):
    url = "https://api.apilayer.com/image_to_text/upload"

    # payload = open(filename, 'rb').read()
    payload = filename
    headers = {
        "apikey": "Jhd5vi1eeDn76jb9h17EQIHmNPC7g7Ts"
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        status_code = response.status_code
        result = response.text
        if status_code == 200:
            return result
        else:
            print("error response code")
            return result
    except:
        print("error api file")