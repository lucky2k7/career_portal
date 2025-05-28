from django.urls import path
from .  import views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name="home"),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('test_page/', views.test_page, name="test_page"),
    path('api/get_question/<int:number>/', views.get_questions, name='get_question'),
    path('api/save_answer/', views.save_user_response, name='save_user_answer'),
    path('api/user_answers/', views.get_user_answers, name='get_user_answers'),
    path('api/mark_review/', views.mark_for_review, name='mark_for_review'),
    path('api/total-questions/', views.get_total_questions, name='get_total_questions'),
]