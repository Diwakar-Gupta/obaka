from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from . import handler
from .models import *
# Create your views here.


def index(request):
    user = auth.get_user(request)
    if user.is_anonymous or not user.is_staff:
        return redirect_to_login(next=request.path)

    return render(request, 'index.html')


def books(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'book.html')


def booksAdd(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    context={}
    if request.method == 'POST':
        context = handler.addBook(request.POST)
    return render(request, 'addBook.html',context=context)


def members(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    allmembers = list(Student.objects.all())
    for f in Faculty.objects.all():
        allmembers.append(f)

    return render(request, 'member.html',context={'members':allmembers})


def notifiedDelayed(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'notifiedDealyed.html')


def circulation(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'circulation.html')


def checkout(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    context = {}
    if request.method == 'POST':
        context = handler.checkout(request.POST)
    return render(request, 'checkout.html' ,context=context)


def checkin(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'checkin.html')


def renew(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'renew.html')


def report(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'report.html')


