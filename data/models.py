from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from .gdrive import upload_to_drive  # Import the Google Drive upload function

class Paper(models.Model):
    REGULATION_CHOICES = [
        ('r-20', 'R-20'),
        ('r-23', 'R-23'),
    ]
    DEPARTMENT_CHOICES = [
        ('cse', 'CSE'),
        ('ece', 'ECE'),
        ('eee', 'EEE'),
        ('mech', 'MECH'),
        ('civil', 'CIVIL'),
    ]
    YEAR_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
    SEMESTER_CHOICES = [('1', '1'), ('2', '2')]
    TYPE_CHOICES = [
        ('mid', 'MID'),
        ('semester', 'SEMESTER'),
        ('questionbank', 'QUESTIONBANK'),
    ]

    regulation = models.CharField(max_length=100, choices=REGULATION_CHOICES, default='r-20')
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default='cse')
    year = models.CharField(max_length=100, choices=YEAR_CHOICES, default='1')
    semester = models.CharField(max_length=100, choices=SEMESTER_CHOICES, default='1')
    paper_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='mid')
    question_paper_name = models.CharField(max_length=100, default='newpaper')

    file_url = models.URLField(blank=True, null=True)  # Store the Google Drive URL

    def save(self, *args, **kwargs):
        file = kwargs.pop("file", None)  # Extract file from arguments

        if file and isinstance(file, InMemoryUploadedFile):
            # Upload the file to Google Drive
            drive_link = upload_to_drive(file, file.name)
            self.file_url = drive_link  # Store Drive link

        super().save(*args, **kwargs)  # Save model instance

    def __str__(self):
        return self.question_paper_name
