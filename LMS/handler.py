from .models import *
from django.shortcuts import get_object_or_404 ,render , render_to_response
from datetime import datetime , timedelta
from django.contrib.contenttypes.models import ContentType

def addBook(request):
    print(request)
    isbnObject=None
    try :
        isbnObject=get_object_or_404(ISBN,isbn=request['isbn'])
    except :
        isbnObject = ISBN(isbn=request['isbn'],author=request['author'],title=request['title'],category=request['category'],publisher=request['publisher'],price=request['price'],quantity=request['quantity'])
        isbnObject.save()
    for _ in range(int(request['quantity'])):
        book = Book(details=isbnObject,active=True,is_issued=False)
        book.save()
    isbnObject.save()
    return render_to_response('checkin.html',context={'success':True})


def checkout(request):
    print(request.POST)
    member = None
    try :
        membertype = request.POST['membertype']
        if membertype == 'Student':
            member = Student.objects.get(id=request.POST['memberid'])
        else:
            member = Faculty.objects.get(id=request.POST['memberid'])
        isbn = ISBN.objects.get(isbn=request.POST['isbn'])
        book = isbn.book_set.filter(is_issued=False).first()
        book.is_issued = True
        duedate = request.POST['duedare'] if request.POST['duedate'] else datetime.now() + timedelta(days=member.settings.maxDay)
        autorenew = True if 'autorenew' in request.POST else False
        from django.contrib import auth
        checkoutfrom = auth.get_user(request).get_username()
        member.count_books += 1
        contentype = ContentType.objects.get_or_create(app_label='LMS', model=membertype)
        if contentype[1]:
            contentype.save()
        contentype = contentype[0]
        issue = Issue(book=book, member_type=contentype, member_id=member.pk, checkoutfrom=checkoutfrom,
                      duedate=duedate, autorenew=autorenew, return_date=None )
        issue.member = member
        isbn.count_issued += 1
        issue.save()
        member.save()
        book.save()
        isbn.save()
    except ISBN.DoesNotExist:
        print('book not exist')
        return (False,{'error':'Book Does not exist','member':member})
    except (Student.DoesNotExist , Faculty.DoesNotExist):
        print('member does not exist')
        return (False,{'error': 'Member Does not exist','member':member})
    return (True,{'success':True,'member':member})



def checkin(request):
    print(request.POST)
    issue = Issue.objects.get(pk=request.POST['pk'])

    return

