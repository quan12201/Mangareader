from .forms import RegistrationForm
from django.http import HttpResponseRedirect 
from django.shortcuts import render, redirect

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mangas:list-mangas')
    return render(request, 'register.html', {'form': form})
