from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from questions.models import Questions

# Create your views here.
# def index(request):
#     return render(request, 'main/layout.html')
def index(request):
    questions = Questions.objects.filter(is_published=True).order_by('-time_create')
    
    return render(request, 'main/index.html', {
        'questions': questions, 
    })

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')


def page_not_found(request, exception): # Функция представления (Обработка исключения 404)
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")