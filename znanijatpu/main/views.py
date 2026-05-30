from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from questions.models import Question, Like
from django.db.models import Count

# Create your views here.
def index(request):
    # 1. Получаем ID вопросов, которые лайкнул текущий пользователь
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list('question_id', flat=True))

    # 2. Получаем опубликованные вопросы + считаем лайки на уровне БД
    questions = Question.objects.filter(is_published=True) \
        .select_related('subsubject__subject', 'author') \
        .annotate(likes_count=Count('likes')) \
        .order_by('-time_create')

    return render(request, 'main/index.html', {
        'questions': questions,
        'liked_ids': liked_ids,
    })

# def index(request):
#     return render(request, 'main/layout.html')
# def index(request):
#     questions = Question.objects.filter(is_published=True).order_by('-time_create')
    
    
#     return render(request, 'main/index.html', {
#         'questions': questions, 
#     })

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')


def page_not_found(request, exception): # Функция представления (Обработка исключения 404)
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")