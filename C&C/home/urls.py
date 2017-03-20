from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^pay/', views.pay, name='pay'),
    url(r'^paid/', views.paid, name='paid'),
]