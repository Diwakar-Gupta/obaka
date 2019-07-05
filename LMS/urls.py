from django.urls import path
from LMS import views


name='LMS'
urlpatterns = [
    path('',views.index,name='index'),

    path('books/',views.books,name='books'),
    path('books/add',views.booksAdd,name='book-add'),

    path('member/',views.member,name='member'),
    path('member/add',views.memberAdd,name='member-add'),
    path('<str:membertype>/<int:memberpk>/',views.member_profile,name='member-profile'),
    path('<str:membertype>/<int:memberpk>/profile',views.member_profile,name='member-profile'),
    path('<str:membertype>/<int:memberpk>/checkout',views.member_checkout,name='member-checkout'),
    path('<str:membertype>/<int:memberpk>/circulation',views.member_circulation,name='member-circulation'),

    path('notifiedDelayed/',views.notifiedDelayed,name='notifiedDelayed'),
    path('report/',views.report,name='report'),

    path('circulation',views.circulation,name='circulation'),
    path('circulation/checkin',views.checkin,name='checkin'),
    path('circulation/renew',views.renew,name='renew'),

    path('demo',views.demo,name='demo'),
]

