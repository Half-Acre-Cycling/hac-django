from django.urls import path
from eliminator import views
from rest_framework import routers

app_name = "eliminator"

urlpatterns = [
    path('upload/', views.upload_page, name="upload_page"),
    path('', views.root_page, name="root_page"),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:pk>', views.categories_detail, name='categories_detail'),
    path('categories/<int:category_id>/round/<int:pk>', views.rounds_detail, name='rounds_detail'),
    path('categories/<int:category_id>/round/<int:round_id>/race/<int:pk>', views.races_detail, name='races_detail'),
    path('categories/<int:category_id>/round/<int:round_id>/race/<int:pk>/scoring/', views.race_scoring, name='race_scoring'),
    path('generate_elim/<int:category_id>', views.generate_first_elim, name='generate_first_elim'),
    path('generate_second_elim/<int:category_id>', views.generate_second_elim, name='generate_second_elim'),
    path('generate_comeback/<int:category_id>', views.generate_comeback, name='generate_comeback'),
    path('generate_final/<int:category_id>/<int:size>', views.generate_final, name='generate_final'),
    path('generate_petit/<int:category_id>/<int:size>', views.generate_petit, name='generate_petit'),
    path('results/csv/<str:year>', views.retrieve_results, name='retrieve_results'),
    # DRF API Views
    path('api/athletes/', views.athlete_list, name="athlete_list"),
    path('api/athletes/<int:pk>', views.athlete_detail, name="athlete_detail"),
    path('api/categories/', views.category_list, name="category_list"),
    path('api/categories/<int:pk>', views.category_detail, name="category_detail"),
    path('api/rounds/', views.round_list, name="round_list"),
    path('api/rounds/<int:pk>', views.round_detail, name="round_detail"),
    path('api/raceresults/', views.race_result_list, name="race_result_list"),
    path('api/raceresults/<int:pk>', views.race_result_detail, name="race_result_detail"),
    path('api/races/', views.race_list, name="race_list"),
    path('api/races/<int:pk>', views.race_detail, name="race_detail"),
    path('categories/<int:category_id>/round/<int:round_id>/race/<int:pk>/demo/', views.demo, name='demo')
]