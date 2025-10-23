from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils.text import slugify
from .models import Student, Parent
from school.models import Notification


def create_notification(user, message):
    
    Notification.objects.create(user=user, message=message)



# -----------------------------
# Add Student
# -----------------------------
def add_student(request):
    if request.method == "POST":
        # Student Fields
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        student_class = request.POST.get('student_class')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image')

        # Parent Fields
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        father_email = request.POST.get('father_email')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        mother_email = request.POST.get('mother_email')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )

        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            student_class=student_class,
            date_of_birth=date_of_birth,
            religion=religion,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )
        create_notification(request.user, f"Added Student: {student.first_name} {student.last_name}")

        messages.success(request, f"Student '{student.first_name} {student.last_name}' added successfully!")
        return redirect('student_list')

    return render(request, "students/add-student.html")


# -----------------------------
# List Students
# -----------------------------
def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    unread_notification = request.user.notification_set.filter(is_read=False)
    context = {
        'student_list': student_list,
        'unread_notification': unread_notification
    }
    return render(request, "students/students.html", context)


# -----------------------------
# View Student
# -----------------------------
def view_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    return render(request, "students/student-details.html", {'student': student})


# -----------------------------
# Edit Student
# -----------------------------
def edit_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent

    if request.method == "POST":
        # Update Student
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.student_id = request.POST.get('student_id')
        student.student_class = request.POST.get('student_class')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.gender = request.POST.get('gender')
        student.religion = request.POST.get('religion')
        student.joining_date = request.POST.get('joining_date')
        student.mobile_number = request.POST.get('mobile_number')
        student.admission_number = request.POST.get('admission_number')
        student.section = request.POST.get('section')
        if request.FILES.get('student_image'):
            student.student_image = request.FILES.get('student_image')

        # Update Parent
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.father_email = request.POST.get('father_email')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.mother_email = request.POST.get('mother_email')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')

        parent.save()
        student.save()
        create_notification(request.user, f"Added Student: {student.first_name} {student.last_name}")

        messages.success(request, f"Student '{student.first_name} {student.last_name}' updated successfully!")
        return redirect('student_list')

    return render(request, "students/edit-student.html", {'student': student, 'parent': parent})


# -----------------------------
# Delete Student
# -----------------------------
def delete_student(request, slug):
    if request.method == "POST":
        student = get_object_or_404(Student, slug=slug)
        student_name = f"{student.first_name} {student.last_name}"
        student.delete()
        create_notification(request.user, f"Deleted student: {student_name}")
        messages.success(request, f"Student '{student_name}' deleted successfully!")
        return redirect('student_list')
    return HttpResponseForbidden("Invalid request method.")
