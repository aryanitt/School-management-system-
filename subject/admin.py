# subject/admin.py

from django.contrib import admin
from .models import Subject  # Import the Subject model

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    # Fields to display in the list view (the main table)
    list_display = (
        'name', 
        'code', 
        'department', 
        'slug'
    )
    
    # Fields used as links to open the change form
    list_display_links = (
        'name', 
        'code'
    )
    
    # Enable search by these fields
    search_fields = (
        'name', 
        'code', 
        'department'
    )
    
    # Fields to filter the list view by (creates a sidebar filter)
    list_filter = (
        'department', 
    )
    
    # Pre-populate the 'slug' field automatically when name or code is typed
    prepopulated_fields = {
        'slug': ('name', 'code',)
    }
    
    # Optional: Define the order of fields on the detail/change form
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'code'),
                'department',
                'description',
                'slug', 
            )
        }),
    )

    # Make the slug read-only so it's not accidentally changed
    readonly_fields = ('slug',)