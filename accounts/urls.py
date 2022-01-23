from django.urls import path
from . import api

urlpatterns = [
    path('api/register/', api.RegisterAPI.as_view()),
    path('api/login/', api.LoginAPI.as_view()),
]
