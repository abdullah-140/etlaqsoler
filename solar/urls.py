from django.urls import path
from . import views

app_name = 'solar'  # يجب أن يكون قبل urlpatterns

urlpatterns = [
path('create-request/', views.create_request, name='create_request'),
path('request/<int:pk>/', views.request_details, name='request_details'),
path('accept-request/<int:request_id>/', views.accept_request, name='accept_request'),
]