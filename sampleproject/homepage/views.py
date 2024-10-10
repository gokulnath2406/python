import qrcode
import base64
import io
from datetime import date, datetime, timedelta
from calendar import monthcalendar
from .models import ElixirModel, create_or_update_user_profile, Attendance
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_otp.decorators import otp_required
from django.shortcuts import render, get_object_or_404, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import GeeksForm, TOTPVerifyForm

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
    print(request.session)
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        return redirect('login_page')
    
    user = get_object_or_404(User, pk=user_id)
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    
    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            if device.verify_token(token):
                login(request, user)
                del request.session['pre_otp_user_id']
                return redirect('dashboard')
            else:
                return HttpResponse("Invalid TOTP token.")
    else:
        form = TOTPVerifyForm()

    return render(request, 'verify_totp.html', {'form': form})

def create_view(request):
    context = {}
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        elixir_instance = form.save()
        username = elixir_instance.name
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{elixir_instance.name}{counter}"
            counter += 1
        User.objects.create_user(username=username, password=elixir_instance.password, email=elixir_instance.email)
        return redirect('add_employee')
    context['form'] = form
    return render(request, "create_view.html", context)

def display_view(request):
    context = {}
    context['dataset'] = ElixirModel.objects.all()
    return render(request, "display_view.html", context)

def detailed_view(request, id):
    context = {}
    context['dataset'] = ElixirModel.objects.get(id=id)
    return render(request, "detailed_view.html", context)

def delete_view(request, id):
    obj = get_object_or_404(ElixirModel, id=id)
    if obj:
        obj.delete()
    return redirect('view_employee')  # Assuming 'view_employee' is the name of the URL pattern

def update_view(request, id):
    context = {}
    obj = get_object_or_404(ElixirModel, id=id)
    form = GeeksForm(request.POST or None, instance=obj)
    if form.is_valid():
        elixir_instance = form.save()
        user = elixir_instance.user
        user.username = elixir_instance.name
        user.set_password(elixir_instance.password)
        user.email = elixir_instance.email
        user.save()
        return redirect('view_employee')
    context["form"] = form
    return render(request, "update_view.html", context)

@login_required
def attendance_calendar(request, year=None, month=None):
    """
    Renders the attendance calendar for a specific employee (logged-in user).

    - Handles GET requests to display the calendar for a specific month (default: current month).
    - Handles POST requests to update attendance for a specific date.

    Args:
        request (HttpRequest): The Django request object.
        year (int, optional): The year for the calendar (defaults to current year).
        month (int, optional): The month for the calendar (defaults to current month).

    Returns:
        HttpResponse: Renders the 'attendance_calendar.html' template with context data.
    """

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
    print(user,"checkkkkkkkkkkkkkkkkkk")
    employee = ElixirModel.objects.all()  # Assuming user has a related Employee

    # Get calendar data for the month
    year, month = selected_date.year, selected_date.month
    month_calendar = monthcalendar(year, month)

    # Get attendance records for the employee and month
    # attendances = Attendance.objects.filter(employee=employee, date__year=year, date__month=month)
    # attendance_dict = {attendance.date.day: attendance.status for attendance in attendances}

    # if request.method == 'POST':
    #     # Handle POST request to update attendance
    #     selected_day = int(request.POST.get('selected_day'))
    #     new_status = request.POST.get('status')  # Expected to be 'present' or 'absent'

    #     # Check for existing attendance record for the day
    #     try:
    #         attendance = Attendance.objects.get(employee=employee.id, date=date(year, month, selected_day))
    #         attendance.status = new_status
    #         attendance.save()
    #     except Attendance.DoesNotExist:
    #         # Create new attendance record if it doesn't exist
    #         Attendance.objects.create(employee=employee, date=date(year, month, selected_day), status=new_status)

    #     # Redirect back to the calendar after updating
    #     return redirect('attendance_calendar', year=year, month=month)

    context = {
        'year': year,
        'month': month,
        'month_calendar': month_calendar,
        'attendance_dict': attendance_dict,
        'today': today,
        'selected_date': selected_date,
    }

    return render(request, 'attendance_calendar.html')
