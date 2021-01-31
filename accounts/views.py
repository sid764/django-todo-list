from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from app.models import Reminder
import datetime
from django.utils import timezone
# Create your views here.

def login(request):
    
    if request.method == 'POST':
    
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
    
        if user is not None:
            auth.login(request, user)
            return redirect('/')
    
        else:
            messages.info(request, 'Invalid credentials, try again')
            return redirect('login')
    
    else:
        return render(request, 'login.html')


def register(request):
    
    if request.method == "POST":
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
           
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username is already taken, try another one')
                return redirect('register')
           
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email was already registered')
                return redirect('register')
           
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User created successfully')
                return redirect('login')
        
        else:
            messages.info(request, 'Passwords did not match')
            return redirect('register')

        return redirect('/')

    else:
        return render(request, 'register.html')


def logout(request):
    
    auth.logout(request)
    return redirect('/')


def see(request):
    
    current_user = request.user
    now = datetime.datetime.now()
    query_result = Reminder.objects.filter(uid=current_user.id, deadline__gte=now).order_by('deadline')
    query_result_over = Reminder.objects.filter(uid=current_user.id, deadline__lte=now).order_by('-deadline')
    context = {'query_result': query_result, 'query_result_over': query_result_over, 'time_now': now}
    
    return render(request, 'see.html', context)


def add(request):
    
    if request.method == 'POST':
        
        current_user = request.user
        now = datetime.datetime.now()
        title = request.POST['title']
        desc = request.POST['desc']
        deadline = request.POST['deadline']
        
        if Reminder.objects.filter(uid=current_user.id, title=title).exists():
            messages.info(request, 'Another instance with same title exists')
            return redirect('add')

        else:
            reminder = Reminder(title=title, desc=desc, deadline=deadline, uid=current_user.id)
            reminder.save()
            return redirect('/')
    
    else:
        return render(request, 'add.html')


def delete(request):
    
    if request.method == 'POST':
        current_user = request.user
        rtitle = request.POST['rtitle']
    
        if Reminder.objects.filter(uid=current_user.id, title=rtitle).exists():
            u_obj = Reminder.objects.get(uid=current_user.id, title=rtitle)
            u_obj.delete()
            return redirect('/')
    
        else:
            messages.info(request, 'That instance did not exist in database')
            return redirect('delete')

    else:
        return render(request, 'delete.html')







