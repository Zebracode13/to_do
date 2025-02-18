from django.db import models
from django.contrib.auth import get_user_model

# Get the default User model
User = get_user_model()
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(blank=True, null=True)  # New field
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title