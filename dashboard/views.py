from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# Import user authentication modules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Import Models
from . import models

# Import Forms
from dashboard.forms import SignupForm

# Signup view
def signup(request):
    """
    Register a new student, login the new user and redirect to breakdowns:index page
    """

    # Check if user already logged
    if request.user.is_authenticated:
        return redirect('dashboard:index')
        
    form_class = SignupForm
    template_name = 'registration/signup.html'

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = False
            # member_group = Group.objects.get(name='member')
            # user.groups.add(member_group,)
            user.save()
            login(request, user)
            return redirect('dashboard:index')
    else:
        form = form_class()
    return render(request, template_name, context={'form': form})

@login_required
def index(request):
    return render(request, 'dashboard/index.html')

def yearbook(request):
    return render(request, 'dashboard/yearbook_form.html', context={})