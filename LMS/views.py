from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from . import handler
# Create your views here.


def index(request):
    user = auth.get_user(request)
    if not user.is_staff:
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
    return render(request, 'member.html')


def notifiedDelayed(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'notifiedDealyed.html')


def issueReturn(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'issueReturn.html')


def issueReturnBook(request,pk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'issueReturn.html')


def issueReturnMember(request,pk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'issueReturn.html')


def report(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'report.html')


