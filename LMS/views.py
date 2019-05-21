from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def books(request):
    return render(request, 'book.html')


def members(request):
    return render(request, 'member.html')


def notifiedDelayed(request):
    return render(request, 'notifiedDealyed.html')


def issueReturn(request):
    return render(request, 'issueReturn.html')


def report(request):
    return render(request, 'report.html')


