from .models import *
from django.shortcuts import get_object_or_404
from datetime import datetime , timedelta
from django.contrib.contenttypes.models import ContentType

def addBook(request):
    print(request)
    isbnObject=None
    try :
        isbnObject=get_object_or_404(ISBN,isbn=request['isbn'])
    except :
        isbnObject = ISBN(isbn=request['isbn'],author=request['author'],title=request['title'],category=request['category'],publisher=request['publisher'],price=request['price'])
        isbnObject.save()
    book = Book(id=request['bookid'],details=isbnObject,active=True,is_issued=False)
    isbnObject.save()
    book.save()
    return {'success':True}


def checkout(request):
    print(request.POST)
    membertype = request.POST['membertype']
    if membertype =='Student' :
        member = Student.objects.get(id=request.POST['memberid'])
    else :
        member = Faculty.objects.get(id=request.POST['memberid'])
    isbn = ISBN.objects.get(isbn=request.POST['isbn'])
    book = isbn.book_set.filter(is_issued=False)[0]
    book.is_issued=True
    duedate = request.POST['duedare'] if request.POST['duedate'] else datetime.now() + timedelta(days=member.settings.maxDay)
    autorenew = True if 'autorenew' in request.POST else False
    from django.contrib import auth
    checkoutfrom = auth.get_user(request).get_username()
    member.count_books += 1
    contentype = ContentType(app_label='LMS', model=membertype)
    contentype.save()
    issue = Issue(book=book,member_type=contentype,checkoutfrom=checkoutfrom,duedate=duedate,autorenew=autorenew)
    issue.member = member
    issue.save()
    member.save()
    book.save()

    return {'success':True}

