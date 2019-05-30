from django.urls import path
from LMS import views


name='LMS'
urlpatterns = [
    path('',views.index,name='index'),

    path('books/',views.books,name='books'),
    path('books/add',views.booksAdd,name='addBook'),

    path('member/',views.member,name='member'),
    path('member/profile',views.member_profile,name='member-profile'),
    path('member/checkout',views.member_checkout,name='member-checkout'),
    path('member/circulation',views.member_circulation,name='member-circulation'),

    path('notifiedDelayed/',views.notifiedDelayed,name='notifiedDelayed'),
    path('report/',views.report,name='report'),

    path('circulation',views.circulation,name='circulation'),
    path('circulation/checkout',views.checkout,name='checkout'),
    path('circulation/checkin',views.checkin,name='checkin'),
    path('circulation/renew',views.renew,name='renew'),

    path('demo',views.demo,name='demo')


]