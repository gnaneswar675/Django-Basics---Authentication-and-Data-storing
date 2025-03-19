from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import StudentDetails
from .forms import StudentForm, RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Home View (Login Page)
def home(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login_success')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'users/home.html', {'form': form})

# Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

# Login Success View
def login_success(request):
    return render(request, 'users/login_success.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student data saved successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'users/create_student.html', {'form': form})

@login_required
def student_list(request):
    students = StudentDetails.objects.all().order_by('-created_at')
    return render(request, 'users/student_list.html', {'students': students})

@login_required
def update_student(request):
    students = StudentDetails.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        student = get_object_or_404(StudentDetails, id=student_id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'users/update_student.html', {'form': form, 'students': students})

def index(request):
    return render(request, 'users/index.html')

