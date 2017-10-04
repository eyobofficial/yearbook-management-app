from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

# Import user authentication modules
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Import Models
from .models import (Yearbook, 
                     StudentYearbook,
                     Poll,
                     PollChoice,
                     Vote,
                     Event,
                     Program,
                     )

# Import Forms
from dashboard.forms import (SignupForm, 
                             YearbookForm, 
                             YearbookSubmitForm,
                             PollForm,
                             )

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
    return render(request, 'dashboard/index.html', {
            'page_name': 'index',
        })

def yearbook(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        if yearbook_detail.submit is not True:
            return redirect('dashboard:yearbook-submit')
        else:
            return render(request, 'dashboard/yearbook.html', {
                    'yearbook': yearbook_detail,
                    'page_name': 'yearbook',
                })

def yearbook_create(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is not None:
        if yearbook_detail.submit is True:
            return redirect('dashboard:yearbook')
        else:
            return redirect('dashboard:yearbook-update')
    else:
        form_class = YearbookForm

        if request.method == 'POST':
            # POST request
            form = form_class(request.POST, request.FILES)

            if form.is_valid():
                form.instance.student = request.user
                form.save()
                return redirect('dashboard:yearbook-submit')
        else:
            # GET Request
            form = form_class()
        return render(request, 'dashboard/yearbook_form.html', context={
                'form': form,
                'page_name': 'yearbook',
            })

def yearbook_update(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        if yearbook_detail.submit is True:
            return redirect('dashboard:yearbook')
        else:
            form_class = YearbookForm

            if request.method == 'POST':
                form = form_class(request.POST, request.FILES, instance=yearbook_detail)

                if form.is_valid():
                    form.save()
                    return redirect('dashboard:yearbook-submit')
            else:
                form = form_class(instance=yearbook_detail)
            return render(request, 'dashboard/yearbook_form.html', {
                    'form': form,
                    'page_name': 'yearbook',
                }) 

def yearbook_submit(request):
    try:
        yearbook_detail = StudentYearbook.objects.get(student=request.user)
    except:
        yearbook_detail = None

    if yearbook_detail is None:
        return redirect('dashboard:yearbook-create')
    else:
        form_class = YearbookSubmitForm

        if request.method == 'POST':
            # POST request
            form = form_class(request.POST)

            if form.is_valid():
                yearbook_detail.submit = True
                yearbook_detail.save()
                return redirect('dashboard:yearbook')
        else:
            # GET Request
            if yearbook_detail.submit is True:
                return redirect('dashboard:yearbook')
            form = form_class()
        return render(request, 'dashboard/yearbook_submit.html', context={
                'form': form,
                'yearbook': yearbook_detail,
                'page_name': 'yearbook',
            })

class PollList(generic.ListView):
    model = Poll

def poll_detail(request, pk):
    # Get a particular poll 
    try:
        poll = Poll.objects.get(pk=pk)
    except:
        poll = None
    
    # Get a Choice List for a specific poll 
    try:
        choice_list = PollChoice.objects.filter(poll_id=pk)
    except:
        choice_list = None

    if request.method == 'POST':
        # POST Request
        choice = request.POST.get('choice')
        if choice is not None:
            # Update Record
            user_vote = Vote(poll=poll, choice_id=choice, student=request.user)
            user_vote.save()
            return redirect('dashboard:index')
    else:
        # GET Request
        try:
            vote = Vote.objects.get(student_id=request.user.id, poll_id=pk)
        except:
            vote = None

        if vote is not None:
            # i.e. User already voted
            return redirect('dashboard:poll-result', poll_id=vote.id)

        if poll is None:
            # No such poll is found
            return redirect('dashboard:poll-list')
    return render(request, 'dashboard/poll_detail.html', {
            'poll': poll,
            'choice_list': choice_list, 
        })

def poll_result(request, pk):
    pass




