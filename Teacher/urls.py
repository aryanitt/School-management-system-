
from django.urls import path
from . import views

urlpatterns = [
    # teachers.html (Teacher List)
    path("", views.teacher_list, name='teacher_list'),
    
    # add-teacher.html (Teacher Add)
    path("add/", views.add_teacher, name="add_teacher"),
    
    # teacher-details.html (Teacher View) - Using slug
    path('details/<str:slug>/', views.view_teacher, name='view_teacher'), 
    
    # edit-teacher.html (Teacher Edit)
    path('edit/<str:slug>/', views.edit_teacher, name='edit_teacher'),
    
    # Optional: Delete Teacher
    # path('delete/<str:slug>/', views.delete_teacher, name='delete_teacher'),
]