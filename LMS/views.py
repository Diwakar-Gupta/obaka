from django.shortcuts import render , render_to_response
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from . import handler
from .models import *
# Create your views here.


def index(request):
    user = auth.get_user(request)
    if user.is_anonymous or not user.is_staff:
        return redirect_to_login(next=request.path)

    return render(request, 'circulation.html')


def books(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    return render(request, 'book.html',context={'isbns':ISBN.objects.all()})


def booksAdd(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    context={}
    if request.method == 'POST':
        context = handler.addBook(request.POST)
    return render(request, 'bookform.html',context=context)


def member(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    members = list(Student.objects.all())
    for f in Faculty.objects.all():
        members.append(f)

    return render(request, 'allMember.html', context={'members':members})


def memberAdd(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request,'memberForm.html')


def member_profile(request,membertype,memberpk):
    member = None
    if membertype == 'Student':
        member = Student.objects.get(pk=memberpk)
    elif membertype == 'Faculty':
        member = Faculty.objects.get(pk=memberpk)

    return render(request,'member/profile.html',context={'member':member})


def member_issue(request,membertype,memberpk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    context = {'member':Student.objects.get(pk=memberpk) if membertype == 'Student' else Faculty.objects.get(pk=memberpk)}

    if request.method == 'POST':
        if membertype.lower() == request.POST['membertype'].lower() and str(memberpk) == request.POST['memberid'].lower():
            context = handler.issue(request)
        else :
            context['error'] = "user dosen't match to request"
    else:
        if membertype == 'Student':
            return render(request,'member/issue.html',context={'member':Student.objects.get(pk=memberpk)})
        elif membertype == 'Faculty':
            return render(request, 'member/issue.html', context={'member': Faculty.objects.get(pk=memberpk)})

    if 'success' in context.values():
        return render_to_response('member/issue.html', context=context)
    else :
        return render(request,'member/issue.html',context=context)


def member_circulation(request,membertype,memberpk):
    context={}
    if membertype == 'Student':
        member = Student.objects.get(pk=memberpk)
        context['member'] = member
        context['issues'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Student),member_id=member.pk)
    elif membertype == 'Faculty':
        member = Faculty.objects.get(pk=memberpk)
        context['member'] = member
        context['issues'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Faculty),member_id=member.pk)
    return render(request,'member/circulation.html',context=context)


def notifiedDelayed(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'notifiedDealyed.html',context={'issues':[x for x in Issue.objects.filter(is_returned=False,autorenew=False) if x.isLate]})


def circulation(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'circulation.html')


def issue(request):
    return render(request,'issue.html')


def returnn(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    return render(request, 'return.html')


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


def demo(request):
    return render(request,'addMember.html')