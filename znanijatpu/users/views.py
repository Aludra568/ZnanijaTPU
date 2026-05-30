from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout as auth_logout
from questions.models import Question, Answer
from .forms import RegisterForm, CustomPasswordChangeForm
from django.utils import timezone
from datetime import timedelta

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()          # сохраняет в БД и хеширует пароль
#             login(request, user)        # автоматический вход
#             return redirect('/')        # редирект на главную
#     else:
#         form = RegisterForm()
#     return render(request, 'users/register.html', {'form': form})

def logout(request):
    auth_logout(request)  # ЭТО ВАЖНО - удаляет сессию!
    return redirect('home')  # редирект на главную

@login_required
def profile(request):
    # Берём только вопросы/ответы текущего пользователя
    user_questions = Question.objects.filter(author=request.user) \
                                     .select_related('subsubject') \
                                     .order_by('-time_create')
                                     
    user_answers = Answer.objects.filter(author=request.user) \
                                 .select_related('question') \
                                 .order_by('-time_create')
                                 
    return render(request, 'users/profile.html', {
        'user_questions': user_questions,
        'user_answers': user_answers,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняет новый хеш пароля
            # Важно: обновляем сессию, чтобы пользователя не "выкинуло" из аккаунта
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            
            messages.success(request, '✅ Пароль успешно изменён!')
            return redirect('users:profile')  # Или 'profile', если нет app_name
    else:
        form = CustomPasswordChangeForm(user=request.user)
        
    return render(request, 'users/change_password.html', {'form': form})

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import VerificationCode
import random

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if user:
            code = str(random.randint(100000, 999999))
            VerificationCode.objects.update_or_create(email=email, defaults={'code': code})
            send_mail('Сброс пароля ZnaniaTPU', f'Код подтверждения: {code}', 
                      settings.DEFAULT_FROM_EMAIL, [email])
            request.session['reset_email'] = email
            request.session.set_expiry(600)  # 10 минут
            return redirect('users:password_reset_confirm')
        messages.warning(request, 'Пользователь с таким email не найден.')
        
    return render(request, 'users/password_reset_request.html')

def password_reset_confirm(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('users:password_reset')

    if request.method == 'POST':
        code = request.POST.get('code')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')

        if p1 != p2:
            messages.error(request, 'Пароли не совпадают.')
        else:
            try:
                vc = VerificationCode.objects.get(email=email, code=code)
                if vc.is_expired:
                    messages.error(request, 'Код истёк. Запросите новый.')
                    del request.session['reset_email']
                    return redirect('users:password_reset')

                user = User.objects.get(email=email)
                user.set_password(p1)
                user.save()
                vc.delete()
                del request.session['reset_email']
                messages.success(request, '✅ Пароль изменён! Войдите с новым паролем.')
                return redirect('users:login')
            except (VerificationCode.DoesNotExist, User.DoesNotExist):
                messages.error(request, 'Неверный код или ошибка данных.')

    return render(request, 'users/password_reset_confirm.html', {'email': email})



# users/views.py
import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .forms import RegisterForm
from .models import VerificationCode

def _send_code(email):
    """Генерация и отправка кода (используется везде)"""
    code = str(random.randint(100000, 999999))
    VerificationCode.objects.update_or_create(email=email, defaults={'code': code})
    send_mail(
        'Код подтверждения ZnaniaTPU',
        f'Ваш код: {code}\nДействует 10 минут.',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True  # ✅ Никогда не ломает сайт
    )
    return code

def register(request):
    VerificationCode.objects.filter(
        created_at__lt=timezone.now() - timedelta(hours=1)
    ).delete()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                messages.error(request, '⚠️ Логин или email уже заняты.')
                return render(request, 'users/register.html', {'form': form})

            _send_code(email)
            request.session['pending_user'] = {
                'username': username,
                'email': email,
                'password': form.cleaned_data['password1']
            }
            request.session.set_expiry(600)
            return redirect('users:verify_registration')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

def verify_registration(request):
    if 'pending_user' not in request.session:
        return redirect('users:register')

    if request.method == 'POST':
        code = request.POST.get('code')
        pending = request.session['pending_user']
        try:
            vc = VerificationCode.objects.get(email=pending['email'], code=code)
            if vc.is_expired:
                messages.error(request, '⏳ Код истёк. Запросите новый.')
                del request.session['pending_user']
                return redirect('users:register')

            user = User.objects.create_user(pending['username'], pending['email'], pending['password'])
            vc.delete()
            del request.session['pending_user']
            login(request, user)
            messages.success(request, '✅ Регистрация успешна!')
            return redirect('home')
        except VerificationCode.DoesNotExist:
            messages.error(request, '❌ Неверный код.')
    return render(request, 'users/verify_code.html', {'email': request.session['pending_user']['email']})

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            _send_code(email)
            request.session['reset_email'] = email
            request.session.set_expiry(600)
            return redirect('users:password_reset_confirm')
        messages.warning(request, '🔍 Пользователь с таким email не найден.')
    return render(request, 'users/password_reset_request.html')

def password_reset_confirm(request):
    email = request.session.get('reset_email')
    if not email: return redirect('users:password_reset')

    if request.method == 'POST':
        code = request.POST.get('code')
        p1, p2 = request.POST.get('password1'), request.POST.get('password2')
        if p1 != p2:
            messages.error(request, 'Пароли не совпадают.')
        else:
            try:
                vc = VerificationCode.objects.get(email=email, code=code)
                if vc.is_expired:
                    messages.error(request, '⏳ Код истёк.')
                    del request.session['reset_email']
                    return redirect('users:password_reset')
                user = User.objects.get(email=email)
                user.set_password(p1)
                user.save()
                vc.delete()
                del request.session['reset_email']
                messages.success(request, '✅ Пароль изменён!')
                return redirect('users:login')
            except (VerificationCode.DoesNotExist, User.DoesNotExist):
                messages.error(request, '❌ Неверный код.')
    return render(request, 'users/password_reset_confirm.html', {'email': email})

# from django.shortcuts import render
# from django.http import HttpResponse

# from .forms import LoginUserForm

# # Create your views here.
# def login_user(request):
#     form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

# def logout_user(request):
#     return HttpResponse("logout")
    

