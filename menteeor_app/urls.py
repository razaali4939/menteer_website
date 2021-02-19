from django.urls import path
from . import views

urlpatterns = [     
	path('wellcome/', views.welcome),
    path('account/', views.account)
]
