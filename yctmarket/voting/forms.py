from django import forms
from django.forms.models import inlineformset_factory
from .models import Department, Course, Assignment
from django.contrib.auth.models import User
from ent.models import Article, Post, InfiniteScroll, Comment, Profile, PhoneNumber

ModuleFormSet = inlineformset_factory(Department, Course, fields=['name'], extra=1, can_delete=True)

ModuleFormSet1 = inlineformset_factory(Course, Assignment, fields=['question', 'option1', 'option2', 'option3', 'option4', 'option5', 'option6', 'option7', 'option8', 'option9', 'option10', 'option11', 'option12', 'option13', 'option14', 'option15', 'option16', 'show_question'], extra=1, can_delete=True)




class VoteForm(forms.ModelForm):
    password1 = forms.CharField(widget = forms.PasswordInput())
    password2 = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            )


    def clean_confirm_password(self):
        password = self.cleaned_data.get('password1')
        confirm_password = self.cleaned_data.get('password2')
        if password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Password Mismatch")
        return email




class VoteFormStudents(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('phone_number', 'matric_number', 'department', 'level', 'photo',)

    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number')
        print(matric_number)
        try:
            confirm = PhoneNumber.objects.filter(matric_number=matric_number)
            print('matric_number')
            print(confirm)
        except:
            confirm = None
            print(matric_number)
        if confirm != None:
            if len(confirm) > 0:
                self.add_error("matric_number", "Matric Number Already Exist")
        return matric_number





class CreateForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('school',
        'name',
        'overview',
        'photo',
        )



class ModuleFormSet2(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ('question',
        'option1',
        'option2',
        'option3',
        'option4',
        'option5',
        'option6',
        'option7',
        'option8',
        'option9',
        'option10',
        'option11',
        'option12',
        'option13',
        'option14',
        'option15',
        'option16',
        )


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('department_access_course',
        )



