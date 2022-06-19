from django.urls import path, include
from user_information import views

app_name = 'user'

urlpatterns =[
     path('create' , views.create_user),
]
