from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout as auth_logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()          # сохраняет в БД и хеширует пароль
            login(request, user)        # автоматический вход
            return redirect('/')        # редирект на главную
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'main/home.html')

def logout(request):
    auth_logout(request)  # ЭТО ВАЖНО - удаляет сессию!
    return redirect('home')  # редирект на главную








# from django.shortcuts import render
# from django.http import HttpResponse

# from .forms import LoginUserForm

# # Create your views here.
# def login_user(request):
#     form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

# def logout_user(request):
#     return HttpResponse("logout")
    

