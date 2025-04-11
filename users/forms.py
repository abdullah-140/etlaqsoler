from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Profile
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from solar.models import User  # استيراد النموذج المخصص بدلاً من User الافتراضي
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # التعديل هنا
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)  # التعديل هنا
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True,
                              widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, required=True,
                              widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    password2 = forms.CharField(max_length=50, required=True,
                              widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True,
                                widget=forms.Select(attrs={'class': 'form-control'}))
    region = forms.CharField(max_length=100, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'Region', 'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=True,
                          widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))

    class Meta:
        model = User  # استخدام النموذج المخصص
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                 'user_type', 'region', 'phone']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
