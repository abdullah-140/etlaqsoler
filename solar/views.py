from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InstallationRequest
from .forms import RequestForm  # تم التعديل هنا

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)  # تم التعديل هنا
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.customer = request.user
            new_request.region = request.user.region
            new_request.save()
            messages.success(request, 'تم إنشاء الطلب بنجاح!')
            return redirect('users:customer_dashboard')
    else:
        form = RequestForm()  # تم التعديل هنا
    
    return render(request, 'solar/create_request.html', {'form': form})

def accept_request(request, request_id):
    if not request.user.is_technician():
        messages.error(request, 'غير مسموح لك بتنفيذ هذا الإجراء')
        return redirect('users:home')
    
    req = get_object_or_404(InstallationRequest, id=request_id, status='pending')
    req.technician = request.user
    req.status = 'accepted'
    req.save()
    
    messages.success(request, 'تم قبول الطلب بنجاح')
    return redirect('users:technician_dashboard')  # استخدم namespace:name


@login_required
def request_details(request, pk):
    """عرض تفاصيل طلب معين"""
    request_obj = get_object_or_404(InstallationRequest, pk=pk, customer=request.user)
    return render(request, 'solar/request_details.html', {'request': request_obj})