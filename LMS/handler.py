from .models import *


def addBook(request):
    print(request)
    isb = ISBN(isbn=request['isbn'],author=request['author'],title=request['title'],category=request['category'],publisher=request['publisher'],price=request['price'])
    isb.save()
    return {'success':True}


def checkout(request):

    return {'success':True}