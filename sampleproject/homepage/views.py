from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import ElixirModel
from .forms import GeeksForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return HttpResponse("incorrect password")
    return render(request, 'login_page.html')
        
def dashboard(request):
    return render(request, 'dashboard.html')

def create_view(request):
    context = {}
    form = GeeksForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_employee') 
    context['form'] = form
    return render(request, "create_view.html", context)
    context['dataset'] = ElixirModel.objects.all()
    return render(request, "display_view.html", context)

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
        form.save()
        return redirect('view_employee')  # Assuming 'view_employee' is the name of the URL pattern
    context["form"] = form
    return render(request, "update_view.html", context)
