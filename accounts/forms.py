from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Question, Option, UserAnswer

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        
class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text', 'is_correct']

class QuestionWithOptionsForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=255, widget=forms.Textarea)

    option1 = forms.CharField(label="Option 1")
    option2 = forms.CharField(label="Option 2")
    option3 = forms.CharField(label="Option 3")
    option4 = forms.CharField(label="Option 4")

    correct_option = forms.ChoiceField(
        label="Correct Option",
        choices=[('1', 'Option 1'), ('2', 'Option 2'), ('3', 'Option 3'), ('4', 'Option 4')],
        widget=forms.RadioSelect
    )

