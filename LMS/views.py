from django.shortcuts import render , render_to_response
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login , HttpResponseRedirect
from . import handler
from .models import *
from datetime import datetime
from django.views.generic.edit import CreateView , UpdateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
    user = auth.get_user(request)
    if user.is_anonymous or not user.is_staff:
        return redirect_to_login(next=request.path)

    return render(request, 'index.html')


def books(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    filtered = [x for x in ISBN.objects.all()]
    print(request.GET)
    if request.method == 'GET':
        if 'author' in request.GET and len(request.GET['author'])>0 :
            filtered = [x for x in filtered if x.author.lower().startswith(request.GET['author'].lower())]
        if 'active' in request.GET:
            if request.GET['active'] == 'yes':
                filtered = filter(lambda x: not x.deactive, filtered)
            if request.GET['active'] == 'no':
                filtered = filter(lambda x: x.deactive, filtered)

    return render(request, 'book.html',context={'isbns':filtered,'filters':request.GET})


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

    filtered = []

    print(request.GET)
    if request.method == 'GET':
        if 'membertype' in request.GET and len(request.GET['membertype']) > 0:
            if request.GET['membertype'] == 'Student':
                filtered.extend([x for x in Student.objects.all()])
            elif request.GET['membertype'] == 'Faculty':
                filtered.extend([x for x in Faculty.objects.all()])
            elif request.GET['membertype'] == 'All':
                filtered.extend([x for x in Student.objects.all()])
                filtered.extend([x for x in Faculty.objects.all()])
        else:
            filtered.extend([x for x in Student.objects.all()])
            filtered.extend([x for x in Faculty.objects.all()])
        if 'idrangemin' in request.GET and len(request.GET['idrangemin']) > 0:
            min = int(request.GET['idrangemin'])
            filtered=filter(lambda x: x.id>=min,filtered)
        if 'idrangemax' in request.GET and len(request.GET['idrangemax']) > 0:
            max = int(request.GET['idrangemax'])
            filtered=filter(lambda x: x.id<=max,filtered)
        if 'active' in request.GET:
            if request.GET['active'] == 'yes':
                filtered = filter(lambda x: x.active, filtered)
            if request.GET['active']=='no':
                filtered = filter(lambda x: not x.active, filtered)
        if 'issued' in request.GET:
            if request.GET['issued'] == 'yes':
                filtered = filter(lambda x: x.issued, filtered)
            if request.GET['issued']=='no':
                filtered = filter(lambda x: not x.issued, filtered)

    return render(request, 'allMember.html', context={'members': filtered, 'filters': request.GET})


def memberAdd(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    return render(request,'memberForm.html',context={'student':UserBasicSetting.objects.filter(type='STUDENT'), 'faculty' : UserBasicSetting.objects.filter(type='FACULTY')})


class StudentAdd(LoginRequiredMixin,CreateView):
    model = Student
    fields = ['name', 'id', 'email']
    template_name = 'formLoop.html'


class FacultyAdd(LoginRequiredMixin,CreateView):
    model = Faculty
    fields = ['name', 'isHOD', 'email']
    template_name = 'formLoop.html'


def member_profile(request,membertype,memberpk):
    member = None
    if membertype == 'STUDENT':
        member = Student.objects.get(pk=memberpk)
    elif membertype == 'FACULTY':
        member = Faculty.objects.get(pk=memberpk)

    return render(request,'member/profile.html',context={'member':member})


def member_issue(request,membertype,memberpk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    context = {'member':Student.objects.get(pk=memberpk) if membertype == 'STUDENT' else Faculty.objects.get(pk=memberpk)}

    if request.method == 'POST':
        if membertype.lower() == request.POST['membertype'].lower() and str(memberpk) == request.POST['memberid']:
            context = handler.issue(request)
        else :
            context['error'] = "user dosen't match to request"
    else:
        if membertype == 'STUDENT':
            return render(request,'member/issue.html',context={'member': Student.objects.get(pk=memberpk), 'holds':Issue.objects.filter(member_type = ContentType.objects.get_for_model(Student), member_id= memberpk, is_returned=False )})
        elif membertype == 'FACULTY':
            return render(request,'member/issue.html',context={'member': Faculty.objects.get(pk=memberpk), 'holds':Issue.objects.filter(member_type = ContentType.objects.get_for_model(Faculty), member_id= memberpk, is_returned=False )})
    if membertype == 'STUDENT':
        context['holds'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Student), member_id=memberpk, is_returned=False)
    elif membertype == 'FACULTY':
        context['holds'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Faculty),member_id=memberpk, is_returned=False)

    if 'success' in context.values():
        return HttpResponseRedirect(reverse('member/issue.html', context=context))
    else :
        return render(request,'member/issue.html',context=context)


def member_circulation(request,membertype,memberpk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    context={}
    if membertype == 'STUDENT':
        member = Student.objects.get(pk=memberpk)
        context['member'] = member
        context['issues'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Student),member_id=member.pk)
    elif membertype == 'FACULTY':
        member = Faculty.objects.get(pk=memberpk)
        context['member'] = member
        context['issues'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(Faculty),member_id=member.pk)
    return render(request,'member/circulation.html',context=context)


def newspaper(request,pk):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    if request.method == 'POST':
        if 'presentToday' in request.POST:
            newspaper = Newspaper.objects.get(pk = pk)
            newspaper.present.add(Date().today())


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

    context = {}
    if request.method=='POST':
        if 'pk' in request.POST:
            context = handler.returnn(request)
        elif 'barcode' in request.POST:
            try:
                isbn = ISBN.objects.get(isbn=int(request.POST['barcode']))
                set = isbn.issue_set.filter(is_returned=False)
                if set:
                    context = {'Issues': set}
                else:
                    context = {'error': 'This item has no Issues'}
            except ISBN.DoesNotExist:
                context = {'error': "Can't find this item"}
    return render(request, 'return.html', context=context)


def renew(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    context = {}
    if request.method=='POST':
        if 'pk' in request.POST:
            context = handler.renew(request)
        elif 'barcode' in request.POST:
            isbn = ISBN.objects.get(isbn=int(request.POST['barcode']))
            set = isbn.issue_set.filter(is_returned=False)
            if set:
                context = {'Issues': set}
            else:
                context = {'error': 'This item has no Issues'}
    return render(request, 'renew.html', context=context)


def report(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    
    return render(request, 'report.html')


def library(request):
    return render(request,'library.html')


def demo(request):
    if 'date' in request.GET :
        print(request.GET)
        dat = datetime.strptime(request.GET['date'],"%y-%m-%d")
        print(type(dat))
        print(dat)

    return render(request,'demo.html')