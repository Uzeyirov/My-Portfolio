from django.urls import path
from . import views

urlpatterns = [
    path('', views.challenge_list, name='challenge_list'),
    path('<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('create/', views.create_challenge, name='create_challenge'),
    path('<int:pk>/delete/', views.delete_challenge, name='delete_challenge'),
    path('submission/<int:sub_pk>/grade/', views.grade_submission, name='grade_submission'),
]