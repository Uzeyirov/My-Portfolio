from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_idea, name='create_idea'),
    path('vote/<int:pk>/', views.vote_idea, name='vote_idea'), # Səsvermə linki
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    # Köhnə 'profile/' yolunu bununla əvəz et:
    path('profile/', views.profile_view, name='profile_self'), # Öz profilin üçün
    path('profile/<str:username>/', views.profile_view, name='profile'), # Başqası üçün

    path('idea/<int:pk>/edit/', views.edit_idea, name='edit_idea'),
    path('idea/<int:pk>/delete/', views.delete_idea, name='delete_idea'),

    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),


    path('idea/<int:pk>/add-solution/', views.add_solution, name='add_solution'),


    path('solution/<int:pk>/delete/', views.delete_solution, name='delete_solution'),
]