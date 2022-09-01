from curses.ascii import HT
from django.shortcuts import render, redirect
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
from eliminator.utils.data_utils import create_data_from_csv
from eliminator.utils import api_functions

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

"""
POST endpoints for updating races/athletes
"""
@require_http_methods(['POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def update_athlete(request):
    print(request.body)
    if 'athlete_id' not in request.POST:
        return HttpResponse('must supply athlete_id', status=400)
    athlete_id = request.POST['athlete_id']
    api_functions.update_athlete(athlete_id, request.data)
    return HttpResponse('OK', status=200)