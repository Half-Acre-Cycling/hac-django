from django.shortcuts import render, redirect
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from .forms import CategoryUploadForm
from eliminator.utils.data_utils import create_data_from_csv

@require_http_methods(['GET', 'POST'])
@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def upload_page(request):
    if request.method == 'POST':
        form = CategoryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            create_data_from_csv(request.FILES['file'], request.POST['category_name'])
            
    form = CategoryUploadForm()
    return render(request, 'upload.html', {'form': form})