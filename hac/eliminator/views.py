from django.shortcuts import render, redirect
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
import pandas as pd

# def handle_uploaded_file(f):
#     with open('file.csv', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def upload_page(request):
    if request.method == 'POST':
        print('post')
        form = CategoryUploadForm(request.POST, request.FILES)
        print(request.FILES['file'])
        if form.is_valid():
            df = pd.read_csv(request.FILES['file'])
            print(df)
            print('valid request')
    form = CategoryUploadForm()
    return render(request, 'upload.html', {'form': form})