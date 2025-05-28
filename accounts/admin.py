from django.contrib import admin
from .models import Profile, Question, Option, UserAnswer
# Register your models here.
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(UserAnswer)
admin.site.register(Profile)

