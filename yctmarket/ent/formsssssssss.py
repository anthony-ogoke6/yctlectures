from django import forms
from django.core.validators import RegexValidator

#class CommentArticle(forms.ModelForm):
	#class Meta:
		#model = models.Article
		#fields = ['title', 'body', 'slug', 'thumb']
from .models import Article, Post, InfiniteScroll, Comment, Profile, PhoneNumber
from shops.models import Product
from shops.models import Stores, Shops
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
    phoneNumber = forms.CharField(required=True, max_length=11)
    def clean_number1(self):
        n = self.cleaned_data.get('phoneNumber')
        print(n)
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



class EmailFormForMeetUp(forms.ModelForm):
    firstname = forms.CharField(required=True, label='First Name',max_length=100)
    lastname = forms.CharField(required=True, label='Last Name', max_length=100)
    address = forms.CharField(required=True, widget=forms.Textarea)
    email = forms.EmailField(required=True)
    phoneNumber = forms.CharField(required=True, max_length=11)
    def clean_number1(self):
        n = self.cleaned_data.get('phoneNumber')
        print(n)
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




class ShopFreeForOneMonth(forms.ModelForm):

    class Meta:
        model = Stores
        fields = ('storename',
        'description',
        'category',
        'logo',
        'status',
        )


class ShopPaymentSixMonth(forms.ModelForm):

    class Meta:
        model = Shops
        fields = ('storename',
        'category',
        'description',
        'logo',
        'status',
        )

class ShopPaymentOneYearMonth(forms.ModelForm):

    class Meta:
        model = Stores
        fields = ('storename',
        'category',
        'description',
        'logo',
        'status',
        )


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


class UploadProductForFree(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'category',
            'title',
            'song',
            'singer',
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




class TutorRegistrationForm(forms.ModelForm):
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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob',)

class ProfileForm1(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('prefix',)


class ProfileFormTutors(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('prefix',)

class ProfileFormStudents(forms.ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ('department',)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
class ReRequestActivationForm(forms.Form):
    email = forms.EmailField(required=True)



class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Comment here!!!', 'rows': '4', 'cols':'50'}))
    class Meta:
        model = Comment
        fields = ('content',)

