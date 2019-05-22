from django.urls import path
from LMS import views


name='LMS'
urlpatterns = [
    path('',views.index),
    path('books/',views.books,name='books'),
    path('members/',views.members,name='members'),

    path('notifiedDelayed/',views.notifiedDelayed,name='notifiedDelayed'),
    path('report/',views.report,name='report'),

    path('issueReturn',views.issueReturn,name='issueReturn'),
    path('issueReturn/book/<int:pk>',views.issueReturnBook,name='issueReturn'),
    path('issueReturn/member/<int:pk>',views.issueReturnMember,name='issueReturn'),

]