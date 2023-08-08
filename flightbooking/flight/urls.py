from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('token',views.token,name='token'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('booking',views.booking,name="booking"),
    path('search',views.search,name="search"),
    path('mybooking',views.mybooking,name="mybooking")
]