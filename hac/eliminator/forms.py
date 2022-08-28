from django import forms

class CategoryUploadForm(forms.Form):
    category_name = forms.CharField(max_length=50)
    file = forms.FileField()
