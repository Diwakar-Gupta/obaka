from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login

# Create your views here.


def index(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'index.html')


def books(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'book.html')


def members(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'member.html')


def notifiedDelayed(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'notifiedDealyed.html')


def issueReturn(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'issueReturn.html')


def report(request):
    print(auth.get_user(request).is_staff)
    return render(request, 'report.html')


