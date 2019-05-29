from .models import *
from django.shortcuts import get_object_or_404

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

    return {'success':True}

