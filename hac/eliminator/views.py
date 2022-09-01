from curses.ascii import HT
from django.shortcuts import render, redirect
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
from eliminator.utils.data_utils import create_data_from_csv
from eliminator.models import Athlete, Category, Race, Round, RaceResult
from eliminator.serializers import AthleteSerializer

@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def upload_page(request):
    if request.method == 'POST':
        form = CategoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            create_data_from_csv(request.FILES['file'], request.POST['category_name'])
            
    form = CategoryUploadForm()
    return render(request, 'upload.html', {'form': form})

def root_page(request):
    user = request.user
    return render(request, 'index.html', {'user': user})

@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def athlete_list(request):
    if request.method == 'GET':
        snippets = Athlete.objects.all()
        serializer = AthleteSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AthleteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def athlete_detail(request, pk):
    try:
        snippet = Athlete.objects.get(pk=pk)
    except Athlete.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AthleteSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AthleteSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
