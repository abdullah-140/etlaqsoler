from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from solar.models import User

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from solar.models import InstallationRequest



def dashboard_redirect(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'customer':
            return redirect('users:customer_dashboard')
        elif request.user.user_type == 'technician':
            return redirect('users:technician_dashboard')
    return redirect('users:home')


@login_required
def customer_dashboard(request):
    if not request.user.is_customer():
        return redirect('users:home')
    
    requests = InstallationRequest.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'users/customer_dashboard.html', {
        'installation_requests': requests
    })

@login_required
@login_required
def technician_dashboard(request):
    if not request.user.is_technician():
        messages.error(request, 'غير مسموح لك بالوصول إلى هذه الصفحة')
        return redirect('users:home')
    
    try:
        accepted_requests = InstallationRequest.objects.filter(
            technician=request.user,
            status='accepted'
        ).order_by('-created_at')
        
        available_requests = InstallationRequest.objects.filter(
            status='pending',
            region=request.user.region
        ).exclude(customer=request.user).order_by('-created_at')
        
        return render(request, 'users/technician_dashboard.html', {
            'accepted_requests': accepted_requests,
            'available_requests': available_requests
        })
        
    except Exception as e:
        messages.error(request, f'حدث خطأ: {str(e)}')
        return redirect('users:home')

def index(request):
    return render(request, 'users/index.html')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = form.cleaned_data['user_type']
            user.region = form.cleaned_data['region']
            user.phone = form.cleaned_data['phone']
            user.save()
            
            messages.success(request, f'Account created for {user.username}')
            return redirect('login')
            
        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users:profile')  # استخدم namespace:name
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
