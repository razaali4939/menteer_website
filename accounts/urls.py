from django.urls import path,include
from . import views

urlpatterns = [
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/',views.password_reset),
    path('passwordChanged/',views.pass_changed_success,name='changed' ),
#    path('index/',views.showindex , name='changed'),
    path('login/', views.manage, name= 'login'),
    path('login/view_mentee/',include('mentee.urls')),
    #path('login/', views.LoginView.as_view(), name='login'),
    path('', views.RegistrationView.as_view(), name='logout'),
    path('login//', views.RegistrationView.as_view(), name='logout'),
    path('logout/',views.logout_request, name='logout'),
    path('check_username/',views.check_username),
    #path('confirmAccount/<uidb64>/<token>/',views.confirmAccount, name= 'activate')
    path('confirmAccount/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('patient/<uuid:id>/', views.manage, name='patient'),
    #path('mentee/', views.signin, name= 'login'),
  #  path('mentee/', views.LoginView, name='login'),
    path('',include('accounts copy.urls')),
    # path('',include('hospital.urls')),
    # path('',include('doctor.urls')),
    # path('',include('patient.urls')),
]
