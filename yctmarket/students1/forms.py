from django import forms
from voting.models import Department


class CourseEnrollForm(forms.Form):
	department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.HiddenInput)