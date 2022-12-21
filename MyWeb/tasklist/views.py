from django.shortcuts import render, redirect
from tasklist.models import Task
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('tasklist:register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('tasklist:register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                return redirect('tasklist:login')
        else:
            messages.info(request, 'password not matched!')
            return redirect('tasklist:register')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Login Successful')
            return redirect('tasklist:home')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('tasklist:login')
    else:
        return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return redirect('tasklist:home')

def insert(request):
    if request.method == 'POST':
        course = request.POST['course']
        description = request.POST['description']
        datetime = request.POST['date'].split('T')
        date = datetime[0]
        time = datetime[1]
        done = False
        task = Task(course=course, description=description, date=date, time=time, done=done, user=request.user)
        task.save()
        return redirect('tasklist:show')
    else:
        return render(request, 'insert.html')

def delete(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('tasklist:show')



def update(request, id):
    print(request)
    if request.method == 'POST':
        print(request)
        task = Task.objects.get(id=id)
        task.description = request.POST['description']
        datetime = request.POST['date'].split('T')
        task.date = datetime[0]
        task.time = datetime[1]
        status = request.POST['status']
        if status == 'Done':
            task.done = True
        task.save()

    return redirect('tasklist:show')

def show(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('id')
        return render(request, 'show.html', {'tasks': tasks})
    else:
        return redirect('tasklist:login')