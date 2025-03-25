from django.db import models
from django.contrib.auth.models import User

# Define the Task Model
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link tasks to users
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title