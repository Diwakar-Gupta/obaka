from .models import *
from django.shortcuts import get_object_or_404 ,render , render_to_response
from datetime import datetime , timedelta ,date
from django.contrib.contenttypes.models import ContentType


def addBook(request):
    print(request)
    isbnObject=ISBN.objects.get_or_create(isbn=request['isbn'])
    print(isbnObject[1])
    if isbnObject[1]:
        isbnObject[0].author = request['author']
        isbnObject[0].title = request['title']
        isbnObject[0].category = request['category']
        isbnObject[0].publisher = request['publisher']
        isbnObject[0].price = request['price']
        isbnObject[0].quantity = request['quantity']
    else :
        isbnObject[0].quantity += int(request['quantity'])

    isbnObject[0].save()

    return {'success':True,'message':"added "+ request['quantity']+" book's with isbn :"+request['isbn']}


def issue(request):
    print(request.POST)
    member = None
    try :
        membertype = request.POST['membertype']
        if membertype == 'STUDENT':
            member = Student.objects.get(id=request.POST['memberid'])
        else:
            member = Faculty.objects.get(id=request.POST['memberid'])
        isbn = ISBN.objects.get(isbn=request.POST['isbn'])

        if isbn.quantity - isbn.deactive -isbn.issued <= 0:
            return {'error': 'No Sufficient Book', 'member': member}

        duedate = request.POST['duedare'] if 'duedate' in request.POST and request.POST['duedate'] else date.today() + timedelta(days=member.settings.maxDay)
        autorenew = True if 'autorenew' in request.POST else False
        from django.contrib import auth
        issuefrom = auth.get_user(request).get_username()
        contentype = ContentType.objects.get_or_create(app_label='LMS', model=membertype)
        if contentype[1]:
            contentype[0].save()
        contentype = contentype[0]
        issue = Issue(book=isbn, member_type=contentype, member_id=member.pk, issuefrom=issuefrom,
                      duedate=duedate, autorenew=autorenew, return_date=None )
        issue.member = member
        isbn.issued += 1
        isbn.count_issues += 1
        issue.save()
        member.issued += 1
        member.count_issues += 1
        member.save()
        isbn.save()
    except ISBN.DoesNotExist:
        print('book not exist')
        return {'error': 'Book Does not exist', 'member': member}
    except (Student.DoesNotExist , Faculty.DoesNotExist):
        print('member does not exist')
        return {'error': 'Member Does not exist','member':member}
    return {'success':True,'member':member}


def returnn(request):
    print(request.POST)
    issue = None
    try :
        issue = Issue.objects.get(pk=request.POST['pk'])
        if issue.is_returned:
            return {'error':'already returned'}
        issue.book.issued -= 1
        issue.member.issued -= 1
        issue.is_returned = True
        issue.return_date = datetime.now()

        if issue.isLate() and not ('forgiveoverdue' in request.POST and len(request.POST['forgiveoverdue'])>0):
            issue.member.fine += issue.fine()

        issue.book.save()
        issue.member.save()
        issue.save()

    except Issue.DoesNotExist:
        return {'error':'this item has no issue history'}

    return {'success' : 'item returned'}


def renew(request):
    print(request.POST)
    issue = None
    try:
        issue = Issue.objects.get(pk=request.POST['pk'])
        if issue.is_returned:
            return {'error': 'already returned'}
        issue.countrenewal += 1
        issue.date = datetime.now()
        issue.duedate = datetime.now() + timedelta(days=issue.member.settings.maxDay)
        issue.save()

    except Issue.DoesNotExist:
        return {'error': 'this item has no issue history'}

    return {'success': 'item renewed'}

def allMember(request):
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
        if 'name' in filters:
            if len(filters['name']) > 0:
                nam = filters['name'].lower()
                filtered = [x for x in filtered if x.name.lower().startswith(nam)]
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
