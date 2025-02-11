from django.urls import path
from .views import generate_mcqs, register_user

urlpatterns = [
    path("generate-mcqs/", generate_mcqs, name="generate_mcqs"),
    path('register/', register_user, name='register_user'),
]
