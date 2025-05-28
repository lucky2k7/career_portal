from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, QuestionForm, OptionForm , QuestionWithOptionsForm
from .models import Option, Question, UserAnswer
from django.forms import modelformset_factory

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import QuestionSerializer, OptionSerializer, UserAnswerSerializer



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.profile.role = form.cleaned_data.get('role')
            user.profile.save()
            messages.success(request, 'Registration is successful. Please login')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.profile.role == 'student':
                    messages.success(request, f'Login successful\nUser:{username}')
                    return redirect('home')
                else:
                    messages.success(request, f'Login successful\nUser:{username}')
                    return redirect('home')
                
                
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')    
@login_required
def home(request):
    home_message = "Home Page"
    return render(request, 'accounts/home.html', {'home_message': home_message})

@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
        # return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'student/dashboard.html')

@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        return redirect('student_dashboard')
        # return HttpResponseForbidden("You are not authorized to access this page.")
    return render(request, 'teacher/dashboard.html')


@login_required
def add_question(request):
    if request.user.profile.role != 'teacher':
        return render(request, 'student/dashboard.html')

    if request.method=='POST':
        form = QuestionWithOptionsForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(text=form.cleaned_data['question_text'])

            options = [
                form.cleaned_data['option1'],
                form.cleaned_data['option2'],
                form.cleaned_data['option3'],
                form.cleaned_data['option4']
            ]
            correct_index = int(form.cleaned_data['correct_option']) - 1
            for i, option in enumerate(options):
                Option.objects.create(
                    question=question,
                    text=option,
                    is_correct=(i == correct_index)
                )
            messages.success(request, 'Question and options added successfully')
            return redirect('teacher_dashboard')
    else:
        form = QuestionWithOptionsForm()
    return render(request, 'teacher/add_question.html', {'form': form})

@login_required
def test_page(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    return render(request, 'student/test_page.html')



# Student response APIS
@api_view(['GET'])
@permission_classes([AllowAny])
def get_questions(request,number):
    # if request.user.profile.role != 'student':
    #     return redirect('teacher_dashboard')
    try:
        question = Question.objects.order_by('id')[number-1]
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    except IndexError:
        return Response({"error": "Question not found"}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def save_user_response(request):
    print("Request data:", request.data)
    # if request.user.profile.role != 'student':
    try:
        question_id = request.data.get('question_id')
        selected_option_id = request.data.get('selected_option_id')

        if not question_id or not selected_option_id:
            return Response({'error': 'Question id and selected option id are required '}, status=400)
        
        question = Question.objects.get(id=question_id)
        selected_option = Option.objects.get(id=selected_option_id)

        answer, created = UserAnswer.objects.update_or_create(
            user = request.user,
            question=question,
            defaults = {'selected_option': selected_option}
        )
        if created:
            print("User answer created:", answer)
            return Response({'message': 'User answer saved successfully'}, status=201)
        else:
            print("User answer updated:", answer)
            return Response({'message': 'User answer updated successfully'}, status=200)
    except Question.DoesNotExist:
        print("Question not found for id:", question_id)
        return Response({'error':'Question mot found'}, status=404)
    except Option.DoesNotExist:
        print("Selected option not found for id:", selected_option_id)
        return Response({'error': 'Selected option not found'}, status=404)
    except Exception as e:
        print("Error:", str(e))
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_answers(request):
    try:
        user_answers = UserAnswer.objects.filter(user=request.user)
        serializer = UserAnswerSerializer(user_answers, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def mark_for_review(request):
    try:
        question_id = request.data.get('question_id')
        question = Question.objects.get(id=question_id)

        answer, created = UserAnswer.objects.get_or_create(
            user=request.user,
            question=question,
        )
        answer.marked_for_review = True
        answer.save()
        return Response({'message': 'Marked for review'})
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)

@api_view(['GET'])
def get_total_questions(request):
    count = Question.objects.count()
    return Response({'total': count})
