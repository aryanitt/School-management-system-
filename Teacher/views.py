# teacher/views.py (Create this new file/app)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
# You need to adjust the import below if Teacher model is in a different app
from .models import Teacher 
from school.models import Notification # Assuming this import is correct

# -----------------------------
# List Teachers (Teacher List)
# -----------------------------

def create_notification(user, message):
    
    Notification.objects.create(user=user, message=message)

    
def teacher_list(request):
    teachers = Teacher.objects.all()
    
    # You might want to pass unread notifications here too for the header
    unread_notification = request.user.notification_set.filter(is_read=False) 
    
    context = {
        'teacher_list': teachers,
        'unread_notification': unread_notification
    }
    return render(request, "teachers/teachers.html", context)


# -----------------------------
# Add Teacher (Teacher Add)
# -----------------------------
def add_teacher(request):
    if request.method == "POST":
        # Teacher Fields (adjust names based on your form)
        teacher = Teacher.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            teacher_id=request.POST.get('teacher_id'),
            gender=request.POST.get('gender'),
            date_of_birth=request.POST.get('date_of_birth'),
            department=request.POST.get('department'),
            qualification=request.POST.get('qualification'),
            joining_date=request.POST.get('joining_date'),
            mobile_number=request.POST.get('mobile_number'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            teacher_image=request.FILES.get('teacher_image')
        )
        
        create_notification(request.user, f"Added Teacher: {teacher.first_name} {teacher.last_name}")

        messages.success(request, f"Teacher '{teacher.first_name} {teacher.last_name}' added successfully!")
        return redirect('teacher_list')

    return render(request, "teachers/add-teacher.html")


# -----------------------------
# View Teacher (Teacher View)
# -----------------------------
def view_teacher(request, slug):
    # Using slug for view_teacher as it's common practice and easier than IDs
    teacher = get_object_or_404(Teacher, slug=slug)
    return render(request, "teachers/teacher-details.html", {'teacher': teacher})


# -----------------------------
# Edit Teacher (Teacher Edit)
# -----------------------------
def edit_teacher(request, slug):
    teacher = get_object_or_404(Teacher, slug=slug)

    if request.method == "POST":
        # Update Teacher fields
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        # ... update all fields here ...
        teacher.email = request.POST.get('email')
        teacher.address = request.POST.get('address')
        if request.FILES.get('teacher_image'):
            teacher.teacher_image = request.FILES.get('teacher_image')

        teacher.save()
        create_notification(request.user, f"Updated Teacher: {teacher.first_name} {teacher.last_name}")

        messages.success(request, f"Teacher '{teacher.first_name} {teacher.last_name}' updated successfully!")
        return redirect('teacher_list')

    return render(request, "teachers/edit-teacher.html", {'teacher': teacher})