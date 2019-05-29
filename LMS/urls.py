from django.urls import path
from LMS import views


name='LMS'
urlpatterns = [
    path('',views.index,name='index'),

    path('books/',views.books,name='books'),
    path('books/add',views.booksAdd,name='addBook'),

    path('members/',views.members,name='members'),

    path('notifiedDelayed/',views.notifiedDelayed,name='notifiedDelayed'),
    path('report/',views.report,name='report'),

    path('circulation',views.circulation,name='circulation'),
    path('circulation/checkout',views.checkout,name='checkout'),
    path('circulation/checkin',views.checkin,name='checkin'),
    path('circulation/renew',views.renew,name='renew'),


]