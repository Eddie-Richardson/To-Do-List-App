from django.db import models
from django.contrib.auth.models import User

# Define the Task Model
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('None', 'None'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link tasks to users
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="None")  # New priority field
    due_date = models.DateField(null=True, blank=True)  # New field for task deadlines


    def __str__(self):
        return self.title
