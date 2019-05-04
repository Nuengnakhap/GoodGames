from django.urls import path

from goodgames import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
]
