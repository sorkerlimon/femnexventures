from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404
from .models import ServiceCategory, Service
import uuid

# Create your views here.

def home_view(request):
    categories = ServiceCategory.objects.all()
    services = Service.objects.all().prefetch_related('images')[:6]  # Show first 6 services with optimized image loading
    context = {
        'categories': categories,
        'services': services,
    }
    return render(request, 'femnexventures_web/home.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('femnexventures_web:home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'femnexventures_web:home')
            messages.success(request, 'Successfully logged in.')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully logged out.')
    return redirect('femnexventures_web:login')

def purchase_detail(request, service_id):
    try:
        # Convert string UUID to UUID object
        service_uuid = uuid.UUID(str(service_id))
        service = get_object_or_404(Service, id=service_uuid)
        return render(request, 'femnexventures_web/purchase_detail.html', {
            'service': service
        })
    except ValueError:
        # Handle invalid UUID format
        raise Http404("Invalid service ID format")
