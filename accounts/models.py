from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

class Question(models.Model):
    text = models.TextField(max_length= 500)
    creted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(max_length= 100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} - {'correct' if self.is_correct else 'incorrect'}"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {self.selected_option.text}"
