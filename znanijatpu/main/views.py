from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')


def page_not_found(request, exception): # Функция представления (Обработка исключения 404)
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")