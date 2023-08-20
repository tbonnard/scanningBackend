import requests
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import json

from ..serializers import PostSerializer
from ..models import Post


class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        imageToTextDetails = imageToTextApiLayer(request.data['image'])
        imageToTextDetailsJson = json.loads(imageToTextDetails)
        # print(imageToTextDetailsJson['lang'])
        if imageToTextDetailsJson is False:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(imageToTextDetailsJson, status=status.HTTP_201_CREATED)

        # posts_serializer = PostSerializer(data=request.data)
        # if posts_serializer.is_valid():
        #     image = posts_serializer.save()
        #     imageToTextDetails = imageToTextApiLayer(image.image)
        #     print(imageToTextDetails)
        #     return Response(imageToTextDetails, status=status.HTTP_201_CREATED)
        # else:
        #     print('error', posts_serializer.errors)
        #     return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#
# def uploadimage(request):
#     if request.method == 'POST':
#         try:
#             print(0)
#             print(request)
#             upload = request.FILES['uploadImage']
#             print(1)
#             fss = FileSystemStorage()
#             file = fss.save(upload.name, upload)
#             file_url = fss.url(file)
#             file_to_text = imageToTextApiLayer(file_url)
#             return JsonResponse({'message': 'received from POST', 'file_to_text':file_to_text }, status=200)
#         except:
#             return JsonResponse({'message':'error'},status=401)
#     return JsonResponse({'message': 'received from GET'}, status=200)



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
        # print(status_code)
        if status_code == 200:
            return result
        else:
            print("error response code")
            return False
    except:
        print("error api file")