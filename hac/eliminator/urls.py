from django.urls import path
from eliminator import views
from rest_framework import routers

app_name = "eliminator"

urlpatterns = [
    path('upload/', views.upload_page, name="upload_page"),
    path('', views.root_page, name="root_page"),
    path('athletes/', views.athlete_list, name="athlete_list"),
    path('athletes/<int:pk>', views.athlete_detail, name="athlete_detail"),
]