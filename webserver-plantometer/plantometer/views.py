from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from django.http import HttpResponseRedirect


# Checks whether user is logged in or not
@login_required(login_url="/users/homepage")
def homepage(request):
    #url(r'^$', RedirectView.as_view(url='/users/')),
    return HttpResponseRedirect('/sensors/data')


# function to render homepage of the website
def home(request):
    return render(request, 'users/index.html')

