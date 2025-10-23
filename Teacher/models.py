# teacher/models.py (Create this new file/app)

from django.db import models
from django.utils.text import slugify

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('other', 'others')])
    date_of_birth = models.DateField()
    department = models.CharField(max_length=50) # Assuming department is a text field
    qualification = models.CharField(max_length=100)
    joining_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    teacher_image = models.ImageField(upload_to='teacher/', blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Creates a slug like "john-doe-T1001"
            self.slug = slugify(f"{self.first_name}-{self.last_name}-{self.teacher_id}")
        super().save(*args, **kwargs)