from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.http import HttpResponse
# relative import of forms
from .models import ElixirModel
from .forms import GeeksForm
from django.shortcuts import redirect



def create_view(request):
	# dictionary for initial data with 
	# field names as keys
	context ={}

	# add the dictionary during initialization
	form = GeeksForm(request.POST or None)
	if form.is_valid():
		form.save()
		
	context['form']= form
	return render(request, "create_view.html", context)

def display_view(request):
	context ={}
	context['dataset']= ElixirModel.objects.all()
	return render(request, "display_view.html", context)

def detailed_view(request, id):
	context ={}
	context['dataset']= ElixirModel.objects.get(id=id)
	return render(request, "detailed_view.html", context)

def delete_view(request, id):
    # dictionary for initial data with 
    # field names as keys
    context ={}
    # # fetch the object related to passed id
    obj = get_object_or_404(ElixirModel, id = id)
    if obj:
        obj.delete()
        #return HttpResponse("Successfuly deleted")
    return redirect('/view_employee')

# update view for details
def update_view(request, id):
    
    # dictionary for initial data with 
    # field names as keys
    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(ElixirModel, id = id)
    # pass the object as instance in form
    form = GeeksForm(request.POST or None, instance = obj)
    print(obj)
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('/view_employee')
    # add form dictionary to context
    context["form"] = form
    return render(request, "update_view.html", context)
