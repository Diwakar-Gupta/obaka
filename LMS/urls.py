from django.urls import path
from LMS import views


name='LMS'
urlpatterns = [
    path('',views.index,name='index'),

    path('books/', views.books, name='books'),
    path('book/<int:pk>', views.book, name='book'),
    path('books/add', views.booksAdd, name='book-add'),

    path('member/',views.member,name='member'),
    path('member/name',views.memberName,name='member-name'),
    path('member/add',views.memberAdd,name='member-add'),

    path('Student/add', views.StudentAdd.as_view(),name= 'student-add'),
    path('Faculty/add', views.FacultyAdd.as_view(), name='faculty-add'),

    path('<str:membertype>/<int:memberpk>/',views.member_profile),
    path('<str:membertype>/<int:memberpk>/profile',views.member_profile,name='member-profile'),
    path('<str:membertype>/<int:memberpk>/issue',views.member_issue, name='member-issue'),
    path('<str:membertype>/<int:memberpk>/circulation',views.member_circulation,name='member-circulation'),

    path('newspaper/<int: pk>',views.newspaper,name = 'newspaper'),

    path('notifiedDelayed/',views.notifiedDelayed,name='notifiedDelayed'),
    path('report/',views.report,name='report'),

    path('circulation',views.circulation,name='circulation'),
    path('circulation/issue',views.issue,name='issue'),
    path('circulation/return',views.returnn,name='return'),
    path('circulation/renew',views.renew,name='renew'),

    path('library',views.library,name='library'),
    path('demo',views.demo,name='demo'),
]

