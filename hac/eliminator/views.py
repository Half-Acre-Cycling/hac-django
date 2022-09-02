from curses.ascii import HT
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
from eliminator.utils.data_utils import create_data_from_csv
from eliminator.models import Athlete, Category, Race, Round, RaceResult
from eliminator.serializers import AthleteSerializer, CategorySerializer, RaceResultSerializer, RaceSerializer, RoundSerializer

@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def upload_page(request):
    if request.method == 'POST':
        form = CategoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            create_data_from_csv(request.FILES['file'], request.POST['category_name'])
            
    form = CategoryUploadForm()
    return render(request, 'upload.html', {'form': form})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def root_page(request):
    user = request.user
    return render(request, 'index.html', {'user': user})

"""
Athletes
"""
@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def athlete_list(request):
    if request.method == 'GET':
        athletes = Athlete.objects.all()
        serializer = AthleteSerializer(athletes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AthleteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def athlete_detail(request, pk):
    try:
        athlete = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AthleteSerializer(athlete)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AthleteSerializer(athlete, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        athlete.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

"""
Categories
"""
@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

"""
Rounds
"""
@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def round_list(request):
    if request.method == 'GET':
        rounds = Round.objects.all()
        serializer = RoundSerializer(rounds, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoundSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def round_detail(request, pk):
    try:
        round = Round.objects.get(pk=pk)
    except Round.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RoundSerializer(round)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RoundSerializer(round, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        round.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

"""
RaceResults
"""
@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def race_result_list(request):
    if request.method == 'GET':
        race_results = RaceResult.objects.all()
        serializer = RaceResultSerializer(race_results, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoundSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def race_result_detail(request, pk):
    try:
        race_result = RaceResult.objects.get(pk=pk)
    except RaceResult.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RaceResultSerializer(race_result)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RaceResultSerializer(race_result, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        race_result.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

"""
Races
"""
@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def race_list(request):
    if request.method == 'GET':
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def race_detail(request, pk):
    try:
        race_result = Race.objects.get(pk=pk)
    except Race.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RaceSerializer(race_result)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RaceSerializer(race_result, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        race_result.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

