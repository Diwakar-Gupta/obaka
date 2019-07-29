from django.shortcuts import render , HttpResponseRedirect , HttpResponse , get_object_or_404 , redirect
from django.contrib import auth
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from . import handler
from .models import *
from datetime import datetime
from django.views.generic.edit import CreateView , UpdateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET, require_POST
import json


def index(request):
    #print(request.META['HTTP_USER_AGENT'])
    user = auth.get_user(request)
    if user.is_anonymous or not user.is_staff:
        return redirect_to_login(next=request.path)

    messages.add_message(request,messages.INFO,'this is message info')
    return render(request, 'index.html')


def books(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)
    filtered = [x for x in ISBN.objects.all()]
    filters = request.GET.copy()
    
    if request.method == 'GET':
        if 'author' in request.GET and len(request.GET['author'])>0 :
            author = request.GET['author'].lower()
            if len(author)<5:
                filtered = [x for x in filtered if x.author.lower().startswith(author)]
            else :
                filtered = [x for x in filtered if author in x.author.lower()]
        if 'title' in request.GET and len(request.GET['title'])>0 :
            title = request.GET['title'].lower()
            if len(title)<5:
                filtered = [x for x in filtered if x.title.lower().startswith(title)]
            else :
                filtered = [x for x in filtered if title in x.title.lower()]
        if 'active' in request.GET:
            if request.GET['active'] == 'yes':
                filtered = [x for x in filtered if not x.deactive]
            if request.GET['active'] == 'no':
                filtered = [x for x in filtered if x.deactive]
        if 'issued' in request.GET:
            if request.GET['issued'] == 'yes':
                filtered = [x for x in filtered if  x.issued]
            if request.GET['issued'] == 'no':
                filtered = [x for x in filtered if not x.issued]
        if 'tissue' in request.GET:
            if request.GET['tissue'] == 'yes':
                filtered = [x for x in filtered if x.count_issues > 0]
            if request.GET['tissue'] == 'no':
                filtered = [x for x in filtered if x.count_issues == 0]
        if 'overdue' in request.GET:
            def islate(l):
                issues = Issue.objects.filter(book=l,is_returned=False,autorenew=False)
                for i in issues:
                    if i.isLate():
                        return True
                return False
            if request.GET['overdue'] == 'yes':
                filtered = [x for x in filtered if islate(x) ]
            if request.GET['overdue'] == 'no':
                filtered = [x for x in filtered if not islate(x)]
        if 'sort' in request.GET and len(request.GET['sort']):
            sortType = request.GET['sort']
            if sortType == 'quantity-up':
                filtered = sorted(filtered , key = lambda x:x.quantity)
            if sortType == 'quantity-down':
                filtered = sorted(filtered , key = lambda x:x.quantity,reverse=True)
            if sortType == 'issued-up':
                filtered = sorted(filtered , key = lambda x:x.issued)
            if sortType == 'issued-down':
                filtered = sorted(filtered , key = lambda x:x.issued,reverse=True)
            if sortType == 'tissue-up':
                filtered = sorted(filtered , key = lambda x:x.count_issues)
            if sortType == 'tissue-down':
                filtered = sorted(filtered , key = lambda x:x.count_issues,reverse=True)
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


def search(request):
    stext=request.GET['stext']
    what = request.GET['what'].lower()
    if what == 'issue' or what=="member":
        try:
            stext = int(request.GET['stext'])
            members = Student.objects.filter(pk=stext)
            go=''
            if what=="issue":
                go = 'member-issue'
            else :
                go = 'member-profile'
            if members.count() == 1:
                return redirect(go,membertype='Student',memberpk=stext)
            members = Faculty.objects.filter(pk=stext)
            if members.count() == 1:
                return redirect(go, membertype='Faculty', memberpk=stext)
        except:
            pass
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/member/?name=' + request.GET['stext'])
    if what == 'return' or what == 'renew':
        try :
            barcode = int(request.GET['stext'])
            isbn = ISBN.objects.get(isbn=barcode)
            set = isbn.issue_set.filter(is_returned=False)
            if set:
                if what == 'renew':
                    return renew(request, {'Issues': set})
                return returnn(request,{'Issues':set})
            else:
                if what == 'renew':
                    return renew(request,{'error': 'This item has no Issues'})
                return returnn(request,{'error': 'This item has no Issues'})
        except ISBN.DoesNotExist:
            if what == 'renew':
                return renew(request, {'error': "Can't find this item"})
            return returnn(request,{'error': "Can't find this item"})
    if what == 'item' :
        try:
            barcode = int(request.GET['stext'])
            isbn = ISBN.objects.get(isbn=barcode)
            return redirect('book',pk=isbn.pk)
        except:
            pass
    return HttpResponse('hjk')


def member(request):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

    return handler.allMember(request)


@require_POST
def memberName(request):
    requested = request.POST['name']
    listS=[]
    if len(requested)<5:
        listS = [x.name for x in Student.objects.all() if x.name.lower().startswith(requested)]
    else :
        listS = [x.name for x in Student.objects.all() if requested in x.name.lower()]
    fl=[]
    for i in listS:
        if i not in fl:
            fl.append(i)
    listS = fl
    
    listF=[]
    if len(requested)<5:
        listF = [x.name for x in Faculty.objects.all() if x.name.lower().startswith(requested)]
    else :
        listF = [x.name for x in Faculty.objects.all() if requested in x.name.lower()]

    fl=[]
    for i in listF:
        if i not in fl:
            fl.append(i)
    listF = fl
    listS.extend(listF)
    list = {'names':listS,'requested':request.POST['name']}
    list = json.dumps(list)
    return HttpResponse(list)


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
    membertype = membertype.lower()
    context = {'member':Student.objects.get(pk=memberpk) if membertype == 'student' else Faculty.objects.get(pk=memberpk)}

    if request.method == 'POST':
        if membertype.lower() == request.POST['membertype'].lower() and str(memberpk) == request.POST['memberid']:
            context = handler.issue(request)
        else :
            context['error'] = "user dosen't match to request"
    context['holds'] = Issue.objects.filter(member_type=ContentType.objects.get_for_model(context['member']),
                                            member_id=memberpk, is_returned=False)
    if context['member'].issued >= context['member'].settings.maxBook:
        context['messages'] = ['member already have maximum book']

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
        context['issues'] = [x for x in Issue.objects.filter(member_type=ContentType.objects.get_for_model(Student),member_id=member.pk)]
    elif membertype == 'FACULTY':
        member = Faculty.objects.get(pk=memberpk)
        context['member'] = member
        context['issues'] = [x for x in Issue.objects.filter(member_type=ContentType.objects.get_for_model(Faculty),member_id=member.pk)]
    if 'have' in request.GET and len(request.GET['have'])>0:
        have = int(request.GET['have'])
        if have >= len(context['issues']):
            return HttpResponse('false')
        def serlise(l):
            d={}
            li=[]
            for i in l:
                d['date']=str(i.date)
                d['title']=i.book.title
                d['author']=i.book.author
                d['barcode']=i.book.isbn
                d['countrenewal']=i.countrenewal
                d['issued_time']=str(i.issued_time)
                d['issuefrom']=i.issuefrom
                d['duedate']=str(i.duedate)
                d['return_date']=str(i.return_date)
                li.append(d)
                d={}
            return li
        data = json.dumps(serlise([x for x in context['issues']][have:have+2]))
        return HttpResponse(data)
    context['issues']=context['issues'][0:7]
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


def issue(request,context={}):
    from django.utils.datastructures import MultiValueDictKeyError
    try:
        type = request.GET['type'].lower()
        id = int(request.GET['id'])
        if type == 'student':
            Student.objects.get(pk=id)
            return redirect('member-issue',membertype=type,memberpk=id)
        if type == 'faculty':
            Faculty.objects.get(pk=id)
            return redirect('member-issue',membertype=type,memberpk=id)
    except MultiValueDictKeyError:
        return render(request, 'issue.html')
    except:
        return render(request, 'issue.html', context={'error': 'cantFind this member'})

    return render(request,'issue.html',context={})


def returnn(request,context={}):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

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


def renew(request,context={}):
    user = auth.get_user(request)
    if not user.is_staff:
        return redirect_to_login(next=request.path)

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
    context={}
    context['books']={}
    total = 0
    issued = 0
    deactive = 0
    for i in ISBN.objects.all():
        total += i.quantity
        issued += i.issued
        deactive += i.deactive
    context['books']['total'] = total
    context['books']['issued'] = issued
    context['books']['deactive'] = deactive

    context['members']={}
    student = Student.objects.all().count()
    faculty = Faculty.objects.all().count()
    deactive = Student.objects.filter(active=False).count() + Faculty.objects.filter(active=False).count()
    total = student + faculty
    context['members']['total'] = total
    context['members']['student'] = student
    context['members']['faculty'] = faculty
    context['members']['deactive'] = deactive

    context['newspaper'] = {}
    context['newspaper']['total'] = Newspaper.objects.all().count()
    context['newspaper']['presenttoday'] = 0
    present = 0
    d = Date.today()
    for n in Newspaper.objects.all():
        if d in n.present.all():
            context['newspaper']['presenttoday'] += 1

    return render(request,'library.html', context=context)


def demo(request):
    if 'date' in request.GET :
        print(request.GET)
        dat = datetime.strptime(request.GET['date'],"%y-%m-%d")
        print(type(dat))
        print(dat)

    return render(request,'demo.html')
