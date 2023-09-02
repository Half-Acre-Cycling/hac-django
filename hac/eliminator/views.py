from datetime import date
import json
# import openpyxl
import pandas as pd
import io
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
from eliminator.utils import data_utils
from eliminator.models import Athlete, Category, Race, Round, RaceResult
from eliminator.serializers import AthleteSerializer, CategorySerializer, RaceResultSerializer, RaceSerializer, RoundSerializer

@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def upload_page(request):
    if request.method == 'POST':
        data_utils.create_data_from_csv(request.FILES['file'], request.POST['category_name'])
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

def demo(request, category_id, round_id, pk):
    if request.method == 'POST':
        placing = json.loads(request.body)
        for classification in placing.keys():
            is_placing = False
            if classification == 'placing_results':
                is_placing = True
            for idx, id in enumerate(placing[classification]):
                result = RaceResult.objects.get(id=id)
                place = idx + 1
                if is_placing:
                    result.place = place
                elif classification == 'unplaced_riders':
                    result.place = ''
                else:
                    result.place = classification.split('_')[0]
                result.is_placing = is_placing
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
    return render(request, 'demo.html', {'round': this_round, 'race': this_race, 'category': this_category, 'race_results': race_results})

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def generate_first_elim(request, category_id):
    category = Category.objects.get(id=category_id)
    data_utils.generate_first_elimination_rounds(category)
    return redirect(f'/categories/{category_id}')

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def generate_second_elim(request, category_id):
    category = Category.objects.get(id=category_id)
    data_utils.generate_second_elimination_rounds(category)
    return redirect(f'/categories/{category_id}')

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def generate_comeback(request, category_id):
    category = Category.objects.get(id=category_id)
    data_utils.generate_comeback_rounds(category)
    return redirect(f'/categories/{category_id}')

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def generate_final(request, category_id, size):
    category = Category.objects.get(id=category_id)
    if size == '16':
        data_utils.generate_final_16(category)
    else:
        data_utils.generate_final_32(category)
    return redirect(f'/categories/{category_id}')

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def generate_petit(request, category_id, size):
    category = Category.objects.get(id=category_id)
    if size == '16':
        data_utils.generate_petit_final_16(category)
    else:
        data_utils.generate_petit_final_32(category)
    return redirect(f'/categories/{category_id}')

def build_result_return_data(athlete, place, category):
    """
    utiltiy function that returns a dict in a format that we
    expect for results placing
    overall category placing can differ from what the place in
    """
    average_points = get_average_points_of_athlete(athlete, category)
    return {
        "id": athlete.id, # only used to detect if a rider has already been placed
        "name": athlete.name,
        "usac_number": athlete.usac_number,
        "bib_number": athlete.bib_number,
        "team": athlete.team,
        "place": place,
        'average_points': average_points
    }

def get_average_points_of_athlete(athlete, category):
    points_map = {
        '1': 13,
        '2': 10,
        '3': 7,
        '4': 5,
        '5': 3,
        '6': 2,
        '7': 1,
        '8': 0
    }
    """
    In an eight person race, points will be assigned as 13, 10, 7, 5, 3, 2, 1, 0
    average points determined by total points divided by number of races entered
    """
    rounds = Round.objects.filter(category=category).exclude(title='Seed')
    races_count = 0
    total_points = 0
    for event_round in rounds:
        races = Race.objects.filter(round=event_round)
        for race in races:
            race_obj = race.serialize()
            if athlete in race_obj['athletes']:
                try:
                    result = RaceResult.objects.get(athlete=athlete, race=race).serialize()
                    if result['is_placing']:
                        races_count += 1
                        place = result['place']
                        if place in points_map.keys():
                            total_points += points_map[place]
                except RaceResult.DoesNotExist:
                    pass
    try:
        average_points = round(total_points / races_count, 2)
    except ZeroDivisionError:
        average_points = 0
    return average_points



def determined_if_athlete_did_not_place(athlete, category):
    rounds = Round.objects.filter(category=category)
    athlete_is_placing = True
    latest_non_placing_reason = '' # there should only be one non-placing reason, but programmatically we're just getting the last
    for round in rounds:
        races = Race.objects.filter(round=round)
        for race in races:
            try:
                result = RaceResult.objects.get(athlete=athlete, race=race).serialize()
                if not result['is_placing']:
                    athlete_is_placing = False
                    latest_non_placing_reason = result['place']
            except RaceResult.DoesNotExist:
                pass
    return {
        'is_placing': athlete_is_placing,
        'reason': latest_non_placing_reason
    }


@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def retrieve_results(request, year):
    """
    How to create results:
    Generate a single CSV which is delimited by Category
    Headers are to be:
    - Athlete Name
    - Athlete USAC Number
    - Athlete Bib Number
    - Athlete Team
    - Place
    - Average Points
    For a given year, iterate over all categories
    First populate top riders by placing from the Final.
    Then populate top riders by placing them from the Petit Final.
    Then see what riders were not placed. 
    If any race one of the riders was in had a non-placing result,
    the rider shall not be placed.
    For all other racers

    """
    categories = Category.objects.filter(year=year)
    output_data = []
    # For a given year, iterate over all categories
    for category in categories:
        category_obj = category.serialize()
        computed_riders_unsorted = []
        non_placing_riders_unsorted = []
        category_data = {
            'name': category_obj['title'],
            'placing_riders_sorted': [],
            'computed_riders_unsorted': [],
            'non_placing_riders_unsorted': []
        }
        # once a rider has been placed, stick them in a list so we know to ignore them
        rider_ids_resolved = []
        try:
            final_round = Round.objects.get(category=category, title='Final')
        except Round.DoesNotExist:
            continue
        final_race = Race.objects.get(round=final_round, title='Final')
        # max_final_place used since race placing does not equal category placing
        max_final_place = 0
        # First populate top riders by placing from the Final.
        for place_number in range(1,21):
            place_str = str(place_number)
            try:
                result = RaceResult.objects.get(race=final_race, place=place_str)
                result_datum = build_result_return_data(result.athlete, place_str, category)
                category_data['placing_riders_sorted'].append(result_datum)
                rider_ids_resolved.append(result_datum['id'])
                max_final_place = place_number
            except RaceResult.DoesNotExist:
                pass
        try:
            petit_final_round = Round.objects.get(category=category, title='Small Final')
            petit_final_race = Race.objects.get(round=petit_final_round, title='Small Final')
            for place_number in range(1,21):
                place_str = str(place_number)
                overall_place = str(1 + max_final_place)
                try:
                    result = RaceResult.objects.get(race=petit_final_race, place=place_str)
                    result_datum = build_result_return_data(result.athlete, overall_place, category)
                    category_data['placing_riders_sorted'].append(result_datum)
                    rider_ids_resolved.append(result_datum['id'])
                    max_final_place = int(overall_place)
                except RaceResult.DoesNotExist:
                    pass
        except Round.DoesNotExist:
            pass
        # Now iterate over athletes, and determine if anyone did not place
        for athlete in category_obj['athletes']:
            if athlete.id in rider_ids_resolved:
                continue
            dnp_result = determined_if_athlete_did_not_place(athlete, category)
            if not dnp_result['is_placing']:
                print(f'found unplacing rider {athlete.name}')
                result_datum = build_result_return_data(athlete, dnp_result['reason'], category)
                non_placing_riders_unsorted.append(result_datum)
                rider_ids_resolved.append(athlete.id)
        for athlete in category_obj['athletes']:
            if athlete.id in rider_ids_resolved:
                continue
            # print(f'attempting to score rider {athlete.name} by points tabulation')
            average_points = get_average_points_of_athlete(athlete, category)
            computed_riders_unsorted.append({
                'id': athlete.id,
                'points': average_points
            })
            rider_ids_resolved.append(athlete.id)
        computed_riders_sorted = sorted(computed_riders_unsorted, key=lambda d: d['points'], reverse=True)
        for rider in computed_riders_sorted:
            athlete = Athlete.objects.get(id=rider['id'])
            # print(f'attempting to score rider {athlete.name} by points tabulation')
            new_place = str(len(category_data['placing_riders_sorted']) + 1)
            result_datum = build_result_return_data(athlete, new_place, category)
            category_data['placing_riders_sorted'].append(result_datum)
        for place in non_placing_riders_unsorted:
            category_data['placing_riders_sorted'].append(place)
        output_data.append(category_data)
    # buffer = io.BytesIO()
    return JsonResponse(output_data, safe=False)
    with pd.ExcelWriter(
        buffer
        # 'output.xslx',
        # mode="a",
        # engine="openpyxl",
        # if_sheet_exists="replace"
    ) as writer:
        for datum in output_data:
            print(datum['name'])
            df = pd.DataFrame(datum['placing_riders_sorted'])
            print(df)
            df.to_excel(writer, sheet_name=output_data['name'], index=False)

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

