from django import forms

#class CommentArticle(forms.ModelForm):
	#class Meta:
		#model = models.Article
		#fields = ['title', 'body', 'slug', 'thumb']
from .models import Article, Post, InfiniteScroll
from django.contrib.auth.models import User


class RequiredFieldsMixin():

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        fields_required = getattr(self.Meta, 'fields_required', None)

        if fields_required:
            for key in self.fields:
                if key not in fields_required:
                    self.fields[key].required = False



class InfiniteScrollForm(forms.ModelForm):

    class Meta:
        model = InfiniteScroll
        fields = (
            'start',
            'end',
            )

class EmailFormForPayment(forms.ModelForm):
    firstname = forms.CharField(required=True, label='First Name',max_length=100)
    lastname = forms.CharField(required=True, label='Last Name', max_length=100)
    address = forms.CharField(required=True, widget=forms.Textarea)
    email = forms.EmailField(required=True)
    phoneNumber = forms.CharField(required=True, label='Phone Number', max_length=11)
    def clean_number1(self):
        n = self.cleaned_data.get('phoneNumber')
        allowed_characters = '0123456789'
        for char in n:
            if char not in allowed_characters:
                raise forms.ValidationError("Please only use digits")
        return n

    email = forms.EmailField(required=True)



    class Meta:
        model = Post
        exclude = ('title',
        'reference',
        'description',
        'bodysnippet',
        'slug',
        'author',
        'category',
        'updated',
        'body',
        'duration',
        'created',
        'image',
        'image2',
        'image3',
        'video',
        'view_count',
        'status',
        'amount',
        )



class EmailFormForMeetUp(forms.ModelForm):
    firstname = forms.CharField(required=True, label='First Name',max_length=100)
    lastname = forms.CharField(required=True, label='Last Name', max_length=100)
    address = forms.CharField(required=True, widget=forms.Textarea)
    phoneNumber = forms.CharField(required=True, label='Phone Number', max_length=11)
    def clean_number1(self):
        n = self.cleaned_data.get('phoneNumber')
        allowed_characters = '0123456789'
        for char in n:
            if char not in allowed_characters:
                raise forms.ValidationError("Please only use digits")
        return n



    class Meta:
        model = Post
        exclude = ('title',
        'reference',
        'description',
        'bodysnippet',
        'slug',
        'author',
        'category',
        'updated',
        'body',
        'duration',
        'created',
        'image',
        'image2',
        'image3',
        'video',
        'view_count',
        'status',
        'amount',
        )



EmailFormForMeetUp


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = (
            'category',
            'title',
            'description',
            'duration',
            'available',
            'amount',
            'image',
            'image2',
            'image3',
            'status',
        )

class PostCreateFormForFree(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'category',
            'title',
            'description',
            'amount',
            'image',
            'image2',
            'image3',
            'available',
            'status',
        )



class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget= forms.TextInput(attrs = {'placeholder':'Username'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs = {'placeholder':'Password'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="", widget = forms.PasswordInput(attrs = {'id': 'pass1','class': 'input100', 'placeholder':'Enter Password Here...'}))
    confirm_password = forms.CharField(label="",  widget = forms.PasswordInput(attrs = {'id': 'pass2', 'class': 'input100'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            )
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password Mismatch")
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Password Mismatch")
        return email


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

#class ProfileEditForm(forms.ModelForm):
#    class Meta:
#        model = Profile
#        exclude = ('user',)
