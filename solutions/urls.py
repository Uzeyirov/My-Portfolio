from django.urls import path
from . import views

urlpatterns = [
    path('', views.solutions_home, name='solutions_home'),
    path('create/', views.create_solution, name='create_solution'),
    path('<int:pk>/', views.solution_detail, name='solution_detail'),
    path('<int:pk>/delete/', views.delete_solution, name='delete_solution'),
    path('<int:pk>/vote/', views.vote_solution, name='vote_solution'),
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
]   