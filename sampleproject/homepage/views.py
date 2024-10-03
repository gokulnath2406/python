import qrcode
import base64
import io
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django_otp.decorators import otp_required
from django.shortcuts import render, get_object_or_404, redirect
from django_otp.plugins.otp_totp.models import TOTPDevice
from .forms import GeeksForm, TOTPVerifyForm
from .models import ElixirModel

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

