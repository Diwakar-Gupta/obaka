from .models import *
from django.shortcuts import get_object_or_404 ,render , render_to_response
from datetime import datetime , timedelta
from django.contrib.contenttypes.models import ContentType
import pytz


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
        if membertype == 'Student':
            member = Student.objects.get(id=request.POST['memberid'])
        else:
            member = Faculty.objects.get(id=request.POST['memberid'])
        isbn = ISBN.objects.get(isbn=request.POST['isbn'])

        if isbn.quantity - isbn.deactive -isbn.issued <= 0:
            return {'error': 'No Sufficient Book', 'member': member}

        duedate = request.POST['duedare'] if 'duedate' in request.POST and request.POST['duedate'] else datetime.now() + timedelta(days=member.settings.maxDay)
        autorenew = True if 'autorenew' in request.POST else False
        from django.contrib import auth
        issuefrom = auth.get_user(request).get_username()
        member.count_books += 1
        contentype = ContentType.objects.get_or_create(app_label='LMS', model=membertype)
        if contentype[1]:
            contentype[0].save()
        contentype = contentype[0]
        issue = Issue(book=isbn, member_type=contentype, member_id=member.pk, issuefrom=issuefrom,
                      duedate=duedate, autorenew=autorenew, return_date=None )
        issue.member = member
        isbn.issued += 1
        issue.save()
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
        issue.member.count_books -= 1
        issue.is_returned = True
        issue.return_date = datetime.now()

        issue.book.save()
        issue.member.save()
        issue.save()

    except Issue.DoesNotExist:
        return {'error':'cant find issue'}

    return {'success' : 'returned book'}


def renew(request):
    print(request.POST)
    issue = None
    try:
        issue = Issue.objects.get(pk=request.POST['pk'])
        if issue.is_returned:
            return {'error': 'already returned'}
        issue.date = datetime.now()
        issue.duedate = datetime.now() + timedelta(days=issue.member.settings.maxDay)

        issue.save()

    except Issue.DoesNotExist:
        return {'error': 'cant find issue'}

    return {'success': 'renewed'}
