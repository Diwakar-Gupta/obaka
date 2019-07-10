from django.shortcuts import render , HttpResponseRedirect , HttpResponse
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from . import handler
from .models import *
from datetime import datetime
from django.views.generic.edit import CreateView , UpdateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
import json

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
    filters = request.GET.copy()
    
    if request.method == 'GET':
        if 'author' in request.GET and len(request.GET['author'])>0 :
            filtered = [x for x in filtered if x.author.lower().startswith(request.GET['author'].lower())]
        if 'active' in request.GET:
            if request.GET['active'] == 'yes':
                filtered = [x for x in filtered if not x.deactive]
            if request.GET['active'] == 'no':
                filtered = [x for x in filtered if x.deactive]
        if 'issued' in request.GET:
            if request.GET['issued'] == 'yes':
                filtered = [x for x in filtered if  x.issued]
            if request.GET['active'] == 'no':
                filtered = [x for x in filtered if not x.issued]
        if 'have' in filters:
            if len(filtered) <= int(filters['have']):
                return HttpResponse('false')
            def serlise(l):
                da={}
                li=[]
                for i in l:
                    da['isbn']=i.isbn
                    da['title']=i.title
                    da['author']=i.author
                    da['quantity']=i.quantity
                    da['issued']=i.issued
                    da['deactive']=i.deactive
                    li.append(da)
                    da={}
                return li
            data = json.dumps(serlise(filtered[int(filters['have']):int(filters['have'])+20]))
            return HttpResponse(data)
    return render(request, 'allBook.html', context={'isbns': filtered[0:20], 'filters':request.GET})


def book(request,pk):
    user = auth.get_user(request)
    if user.is_anonymous or not user.is_staff:
        return redirect_to_login(next=request.path)

    isbn = ISBN.objects.get(pk=pk)
    return render(request,'bookDetail.html',context={'isbn':isbn})
    


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

    filters = request.GET.copy()
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
            filtered = [x for x in filtered if x.id >= min]
        if 'idrangemax' in request.GET and len(request.GET['idrangemax']) > 0:
            max = int(request.GET['idrangemax'])
            filtered = [x for x in filtered if x.id<=max]
        if 'active' in request.GET:
            if request.GET['active'] == 'yes':
                filtered = [x for x in filtered if x.active]
            if request.GET['active']=='no':
                filtered = [x for x in filtered if not x.active]
        if 'issued' in filters:
            if filters['issued'] == 'yes':
                filtered = [x for x in filtered if x.issued]
            if filters['issued']=='no':
                filtered = [x for x in filtered if not x.issued]
        if 'overdue' in request.GET:
            def checklate(j):
                for i in j:
                    if i.isLate():
                        return True
                return False
            if request.GET['overdue'] == 'yes':
                filtered = [x for x in filtered if checklate(
                    Issue.objects.filter(member_type=ContentType.objects.get_for_model(x), member_id=x.pk,
                                         is_returned=False))]
            if request.GET['overdue']=='no':
                filtered = [x for x in filtered if not checklate(Issue.objects.filter(member_type=ContentType.objects.get_for_model(x),member_id=x.pk,is_returned=False))]
        if 'fine' in request.GET:
            if request.GET['fine'] == 'no':
                filtered = [x for x in filtered if x.fine<=0]
            if request.GET['fine'] == 'yes':
                filtered = [x for x in filtered if x.fine > 0]
        if 'have' in filters:
            if len(filtered) <= int(filters['have']):
                return HttpResponse('false')
            def serlise(l):
                da={}
                li=[]
                for i in l:
                    da['id']=i.id
                    da['name']=i.name
                    da['type']=i.settings.type
                    da['active']=i.active
                    da['issued']=i.issued
                    li.append(da)
                    da={}
                return li
            data = json.dumps(serlise(filtered[int(filters['have']):int(filters['have'])+20]))
            print(data)
            return HttpResponse(data)

    return render(request, 'allMember.html', context={'members': filtered[0:13], 'filters': filters})


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
    context['mode'] = 'return'
    return render(request, 'renewreturn.html', context=context)


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
    context['mode'] = 'renew'
    return render(request, 'renewreturn.html', context=context)


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
