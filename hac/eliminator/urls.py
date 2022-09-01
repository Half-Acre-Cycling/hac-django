from django.urls import path
from eliminator import views

app_name = "eliminator"

urlpatterns = [
    path('upload/', views.upload_page, name="upload_page"),
    path('', views.root_page, name="root_page")
]