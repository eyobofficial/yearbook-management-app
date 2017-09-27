from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from . import models

from .forms import TestForm

def index(request):
    return render(request, 'dashboard/index.html')

class YearbookView(CreateView):
    pass


