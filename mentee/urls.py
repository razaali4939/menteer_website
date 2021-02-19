from django.urls import path
from . import views

urlpatterns = [
   #path('mentee/<uuid:id>/', views.mentee_view, name='mentee'),
   path('<uuid:id>/', views.mentee_view, name='mentee'),
   path('', views.editMentee, name='mentee'),
   # path('', views.mentee_view, name='mentee'),
   # path('mentee/', views.mentee_view, name='mentee'),
   # path('mentee/', views.mentee_view, name='mentee'),
 #  path('editMentee/<uuid:id>/',views.editMentee),
    path('showmentee/',views.showmentee),
    path('<uuid:id>/editmentee/',views.editMentee),
    path('passwordChange/<uuid:id>/',views.passwordChange),
    path('getwatingappointments/<uuid:id>/',views.getwatingappointments),
    path('list/<uuid:id>/',views.get_list),
]