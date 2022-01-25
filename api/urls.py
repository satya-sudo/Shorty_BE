from api import views
from django.urls import path
urlpatterns = [
    path('auth/register/',view=views.RegisterUser.as_view()),
    path('auth/login/',view=views.LoginAPIView.as_view()),
    path('url/',view=views.UrlList.as_view()),
]
