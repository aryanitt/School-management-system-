# teacher/admin.py

from django.contrib import admin
from .models import Teacher # Import your Teacher model

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # Fields to display in the list view (the table)
    list_display = (
        'teacher_id', 
        'first_name', 
        'last_name', 
        'email', 
        'department', 
        'joining_date'
    )
    
    # Fields to use as links to the change page
    list_display_links = (
        'teacher_id', 
        'first_name', 
        'last_name'
    )
    
    # Enable search by these fields
    search_fields = (
        'first_name', 
        'last_name', 
        'teacher_id', 
        'email'
    )
    
    # Fields to filter the list view by (creates a sidebar filter)
    list_filter = (
        'department', 
        'gender', 
        'joining_date'
    )
    
    # Pre-populate the 'slug' field automatically from first_name, last_name, and teacher_id
    prepopulated_fields = {
        'slug': ('first_name', 'last_name', 'teacher_id',)
    }
    
    # Define the fields shown on the detail/change page
    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('first_name', 'last_name'), 
                ('teacher_id', 'email'),
                ('gender', 'date_of_birth'),
                'teacher_image',
            )
        }),
        ('Academic & Contact Details', {
            'fields': (
                'department',
                'qualification',
                'joining_date',
                'mobile_number',
                'address',
                'slug', # Keep slug visible but non-editable if needed
            )
        }),
    )

    # Optional: Make the slug read-only to prevent manual changes after creation
    readonly_fields = ('slug',)