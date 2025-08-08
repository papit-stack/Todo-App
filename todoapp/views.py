from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home(request):
    if request.method=="POST":
        task=request.POST.get('task')
        todo=Todo(user=request.user,name=task)
        todo.save()
        return redirect('home')
    all_todo=Todo.objects.filter(user=request.user)
    return render(request,'todoapp/todo.html',{'todo':all_todo})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        #username
        if len(username)<2:
            messages.error(request,"Username must be at least 3 character")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('register')
        #password
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')
        if not any(c.isdigit() for c in password):
            messages.error(request, "Password must contain at least one number.")
            return redirect('register')
        if not any(c.isupper() for c in password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return redirect('register')
        if not any(c.islower() for c in password):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return redirect('register')
        if not any(c in "!@#$%^&*()_+-=[]{}|;':\",.<>?/`~" for c in password):
            messages.error(request, "Password must contain at least one special character.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request,"User registered successfully")
        return redirect('login')
        
    return render(request,'todoapp/register.html')

def login_view(request):
    if request.method=="POST":
        username=request.POST.get('uname')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Incorrect credentials")
            return  redirect('login')

    return render(request,'todoapp/login.html')
@login_required
def delete_task(request,id):
    task=get_object_or_404(Todo,id=id,user=request.user)
    task.delete()
    return redirect('home')
@login_required
def update_task(request,id):
    task=get_object_or_404(Todo,id=id,user=request.user)
    task.status=True
    task.save()
    return redirect('home')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')