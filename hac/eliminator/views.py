from datetime import date
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

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def categories(request):
    current_categories = Category.objects.filter(year=date.today().year)
    category_data = []
    for category_query_obj in current_categories:
        category = category_query_obj.serialize()
        athlete_count = category_query_obj.athletes.all().count()
        category_data.append({
            'id': category['id'],
            'title': category['title'],
            'athlete_count': athlete_count
        })
    return render(request, 'categories.html', {'category_data': category_data})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def categories_detail(request, pk):
    this_category = Category.objects.get(id=pk)
    athletes = this_category.athletes.all()
    athlete_count = athletes.count()
    category = this_category.serialize()
    category_datum = {
        'id': category['id'],
        'title': category['title'],
        'athlete_count': athlete_count,
        'year': category['year']
    }
    athlete_data = []
    for athlete_obj in athletes:
        athlete_data.append(athlete_obj.serialize())
    round_data = []
    rounds = Round.objects.filter(category=this_category)
    for round in rounds:
        round_data.append(round.serialize())
    return render(request, 'categories_detail.html', {'category_datum': category_datum, 'athlete_data': athlete_data, 'round_data': round_data})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def rounds_detail(request, category_id, pk):
    this_category = Category.objects.get(id=category_id).serialize()
    this_round = Round.objects.get(id=pk)
    races = Race.objects.filter(round=this_round)
    race_data = []
    for race in races:
        race_data.append(race.serialize())
    return render(request, 'rounds_detail.html', {'round': this_round.serialize(), 'race_data': race_data, 'category': this_category})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def races_detail(request, category_id, round_id, pk):
    this_category = Category.objects.get(id=category_id).serialize()
    this_round = Round.objects.get(id=round_id).serialize()
    this_race = Race.objects.get(id=pk).serialize()
    return render(request, 'races_detail.html', {'round': this_round, 'race': this_race, 'category': this_category})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def race_scoring(request, category_id, round_id, pk):
    if request.method == 'POST':
        result = RaceResult.objects.get(id=request.POST['id'])
        place = request.POST['place']
        result.place = place
        result.is_placing = place.isdigit()
        result.save()
    this_category = Category.objects.get(id=category_id).serialize()
    this_round = Round.objects.get(id=round_id).serialize()
    this_race_obj = Race.objects.get(id=pk)
    this_race = this_race_obj.serialize()
    race_results = []
    for athlete_obj in this_race_obj.athletes.all():
        athlete= athlete_obj.serialize()
        race_result, created = RaceResult.objects.get_or_create(
            athlete=athlete_obj,
            race=this_race_obj
        )
        race_results.append(race_result)
    return render(request, 'races_scoring.html', {'round': this_round, 'race': this_race, 'category': this_category, 'race_results': race_results})

"""
DRF Views
"""

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


@api_view(['GET', 'PUT', 'DELETE'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
@csrf_exempt
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

