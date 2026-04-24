# teams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_list, name='team_list'),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/apply/', views.send_join_request, name='send_join_request'),
    path('my-requests/', views.manage_requests, name='manage_requests'),
    path('request/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('request/<int:request_id>/reject/', views.reject_request, name='reject_request'),  
    path('workspace/<int:team_id>/', views.team_workspace, name='team_workspace'),
    path('send_message/<int:team_id>/', views.send_message, name='send_message'),
    # teams/urls.py
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    # teams/urls.py
    path('leave-team/<int:team_id>/', views.leave_team, name='leave_team'),
    path('remove-member/<int:team_id>/<int:user_id>/', views.remove_member, name='remove_member'),
    
]