from django.urls import path
from .views import uploadFileViews, csrfTokenViews, propertyViews, messageViews, claimViews
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('get-csrf-token/', csrf_exempt(csrfTokenViews.get_csrf_token), name='get_csrf_token'),
    path('uploadimage/', uploadFileViews.PostView.as_view(), name='posts_list'),
    path('property/', propertyViews.PropertyView.as_view()),
    path('property/<int:pk>/', propertyViews.PropertyDetailsView.as_view()),
    path('messages/<str:number>/', messageViews.MessagesView.as_view()),
    path('message/', messageViews.MessageView.as_view()),
    path('message/<int:pk>/', messageViews.MessageDetailsView.as_view()),
    path('claim/', claimViews.ClaimView.as_view()),
    path('claim/<int:pk>/', claimViews.ClaimDetailsView.as_view()),
]
