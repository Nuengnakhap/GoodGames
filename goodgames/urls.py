from django.urls import path

from goodgames import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),
    path('tournament/', views.tournament, name='tournament'),
    path('tournament/<int:tour_id>/', views.tournament_info, name='tournament_info'),
    path('team/<int:team_id>/', views.team_info, name='team_info')
]
