# subject/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Subject List (subjects.html)
    path("", views.subject_list, name='subject_list'),
    
    # Subject Add (add-subject.html)
    path("add/", views.add_subject, name="add_subject"),
    
    # Subject Edit (edit-subject.html)
    path('edit/<str:slug>/', views.edit_subject, name='edit_subject'), 
    
    # Optional: Delete Subject 
    path('delete/<str:slug>/', views.delete_subject, name='delete_subject'),
]