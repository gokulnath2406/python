import qrcode
import base64
import io
import os 
from datetime import date, datetime, timedelta
from calendar import monthcalendar
from .models import ElixirModel, create_or_update_user_profile, Attendance
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django_otp.decorators import otp_required
from django.shortcuts import render, get_object_or_404, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import GeeksForm, TOTPVerifyForm
from django.core.files.storage import FileSystemStorage

@login_required
def setup_totp(request):
    user = request.user
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    if device:
        return HttpResponse("TOTP already configured.")

    if request.method == 'POST':
        device = TOTPDevice.objects.create(user=user, confirmed=True)
        return redirect('dashboard')

    device = TOTPDevice.objects.create(user=user, confirmed=False)
    uri = device.config_url
    img = qrcode.make(uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode('ascii')

    return render(request, 'setup_totp.html', {'qr_code': img_str})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                request.session['pre_otp_user_id'] = user.id
                return redirect('verify_totp')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponse("Invalid login.")
    return render(request, 'login_page.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def verify_totp(request):
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login_page')

    user = get_object_or_404(User, pk=user_id)
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

    if not device:
        return HttpResponse("No TOTP device found for user.")

    error_message = None
    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            if device.verify_token(token):
                login(request, user)
                request.session.pop('pre_otp_user_id', None)
                return redirect('dashboard')
            else:
                error_message = "Invalid TOTP token."
    else:
        form = TOTPVerifyForm()

    return render(request, 'verify_totp.html', {'form': form, 'error_message': error_message})

@login_required
def create_view(request):
    context = {}
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        elixir_instance = form.save(commit=False)
        username = elixir_instance.name
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{elixir_instance.name}{counter}"
            counter += 1
        # Create a new User instance
        user = User.objects.create_user(username=username, password=elixir_instance.password, email=elixir_instance.email)
        
        # Assign the user to the corresponding group (designation)
        group = elixir_instance.designation
        user.groups.add(group)
        
        # Save the employee instance after creating the user to ensure the user object is available
        elixir_instance.user = user
        elixir_instance.save()
        
        return redirect('add_employee')
    context['form'] = form
    return render(request, "create_view.html", context)

@login_required
def display_view(request):
    context = {}
    context['dataset'] = ElixirModel.objects.all()
    return render(request, "display_view.html", context)

@login_required
def detailed_view(request, id):
    employee = get_object_or_404(ElixirModel, id=id)
    dataset = {
        'name': employee.name,
        'designation': employee.designation.name if employee.designation else None,  # Assuming designation is a ForeignKey to Group
        'phone_number': employee.phone_number,
        'salary': employee.salary,
        'personal_email': employee.personal_email,
        'email': employee.email,
        'photo_url': employee.photo.url if employee.photo else None,
        'marital_status': employee.marital_status.status if employee.marital_status else 'Not specified',
        'date_of_birth': employee.date_of_birth.strftime('%Y-%m-%d') if employee.date_of_birth else 'Not specified'
    }
    return render(request, "detailed_view.html", {'dataset': dataset})

    
    context = {}
    obj = get_object_or_404(ElixirModel, id=id)
    if form.is_valid():
        user.save()

@login_required
def delete_view(request, id):
    obj = get_object_or_404(ElixirModel, id=id)
    if obj:
        obj.delete()
    return redirect('view_employee')  # Assuming 'view_employee' is the name of the URL pattern

@login_required
def update_view(request, id):
    context = {}
    obj = get_object_or_404(ElixirModel, id=id)
    if request.method == 'POST':
        form = GeeksForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            elixir_instance = form.save()
            user = elixir_instance.user
            user.username = elixir_instance.name
            user.set_password(elixir_instance.password)
            user.email = elixir_instance.email
            user.save()
            
            # Handle file upload
            if 'photo' in request.FILES:
                photo = request.FILES['photo']
                fs = FileSystemStorage()
                filename = fs.save(photo.name, photo)
                elixir_instance.photo = fs.url(filename)
                elixir_instance.save()
            
            return redirect('view_employee')
    else:
        form = GeeksForm(instance=obj)

    context["form"] = form
    context["object"] = obj
    return render(request, "update_view.html", context)

@login_required
def attendance_calendar(request, year=None, month=None):
    # Get current date or specified year/month
    today = date.today()
    if year and month:
        try:
            year = int(year)
            month = int(month)
            if 1 <= month <= 12:
                selected_date = date(year, month, 1)  # Set 1st day of the month
            else:
                # Handle invalid month - redirect to current month
                return redirect('attendance_calendar')
        except ValueError:
            # Handle invalid year/month format - redirect to current month
            return redirect('attendance_calendar')
    else:
        selected_date = today

    # Get employee (logged-in user)
    user = request.user.id  # Assuming user is linked to an Employee model
    employee = ElixirModel.objects.all()  # Assuming user has a related Employee

    # Get calendar data for the month
    year, month = selected_date.year, selected_date.month
    month_calendar = monthcalendar(year, month)

    context = {
        'year': year,
        'month': month,
        'month_calendar': month_calendar,
        'attendance_dict': attendance_dict,
        'today': today,
        'selected_date': selected_date,
    }

    return render(request, 'attendance_calendar.html')
