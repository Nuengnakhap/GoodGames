from django.urls import path

from dayoff import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create-dayoff'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),
]
