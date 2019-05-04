from django.urls import path

from polls import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:poll_id>/', views.detail, name='poll_detail'),
    path('detail/<int:poll_id>/create-comments/', views.comment, name='poll_comment'),
    path('detail/<int:poll_id>/question/', views.create_question, name='poll_question'),
    path('create/', views.create_poll, name='create_poll'),
    path('login/', views.mylogin, name='login'),
    path('logout/', views.mylogout, name='logout'),
    path('detail/<int:poll_id>/update/', views.update_poll, name='update_poll'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
    path('detail/<int:poll_id>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('detail/<int:poll_id>/question/<int:question_id>/choice/', views.add_choice, name='edit_choice'),
    path('detail/<int:poll_id>/question/<int:question_id>/choice/api', views.add_choice_api, name='add_choice_api'),
]
