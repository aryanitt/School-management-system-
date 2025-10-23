# subject/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Subject 
# Assuming create_notification is defined and accessible
from school.models import Notification
def create_notification(user, message):
    
    Notification.objects.create(user=user, message=message)


# --- List Subjects (Subject List) ---
@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    # Assuming notification context is passed via custom middleware or base view
    context = {'subject_list': subjects}
    return render(request, "subjects/subjects.html", context)

# --- Add Subject (Subject Add) ---
@login_required
def add_subject(request):
    if request.method == "POST":
        try:
            subject = Subject.objects.create(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                department=request.POST.get('department'),
                description=request.POST.get('description'),
            )
            create_notification(request.user, f"Added Subject: {subject.name}")
            messages.success(request, f"Subject '{subject.name}' added successfully!")
            return redirect('subject_list')
        
        except Exception as e:
            messages.error(request, f"Error adding subject: {e}")
            return redirect('add_subject')

    return render(request, "subjects/add-subject.html")

# --- Edit Subject (Subject Edit) ---
@login_required
def edit_subject(request, slug):
    subject = get_object_or_404(Subject, slug=slug)

    if request.method == "POST":
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.department = request.POST.get('department')
        subject.description = request.POST.get('description')
        
        subject.save()
        create_notification(request.user, f"Updated Subject: {subject.name}")
        messages.success(request, f"Subject '{subject.name}' updated successfully!")
        return redirect('subject_list')

    return render(request, "subjects/edit-subject.html", {'subject': subject})

# --- Delete Subject ---
@login_required
def delete_subject(request, slug):
    if request.method == "POST":
        subject = get_object_or_404(Subject, slug=slug)
        subject_name = subject.name
        subject.delete()
        
        create_notification(request.user, f"Deleted subject: {subject_name}")
        messages.success(request, f"Subject '{subject_name}' deleted successfully!")
        return redirect('subject_list')
        
    return HttpResponseForbidden("Invalid request method.")