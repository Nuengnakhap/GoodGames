from django.urls import path

from goodgames import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),
    path('tournament/', views.tournament, name='tournament'),
    path('tournament/create/', views.create_tournament, name='create_tournament'),
    path('tournament/<int:tour_id>/', views.tournament_info, name='tournament_info'),
    path('tournament/<int:tour_id>/bracket', views.tournament_bracket, name='tournament_bracket'),
    path('tournament/<int:tour_id>/manage', views.manage_tournament, name='manage_tournament'),
    path('team/<int:team_id>/', views.team_info, name='team_info'),
    path('team/<int:team_id>/match/', views.match_team, name='match_team'),
    path('team/create/', views.create_team, name='create_team'),
    path('ranking/', views.ranking, name='ranking'),
    path('team/', views.team, name='team'),
    path('team/<int:team_id>/manage/', views.manage_team, name='manage_team'),
    path('manage_player/', views.manage_player, name='manage_player'),
    path('team/<int:team_id>/match/<int:match_id>/', views.notice_result, name='notice_result'),
    path('404/', views.error404, name='error'),
]
