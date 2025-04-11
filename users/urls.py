from django.urls import path
from .views import (
    home, 
    profile,  # تأكد من وجود هذه الوظيفة مستوردة
    RegisterView,
    dashboard_redirect, 
    customer_dashboard,
    technician_dashboard
)

app_name = 'users'  # إضافة namespace للتطبيق

urlpatterns = [
    path('', home, name='home'),
    
    path('register/', RegisterView.as_view(), name='register'),
path('profile/', profile, name='profile'),  # الاسم الصحيح هو 'profile'
path('dashboard/', dashboard_redirect, name='dashboard-redirect'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('technician-dashboard/', technician_dashboard, name='technician_dashboard'),
]