from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'questions/index.html')

def question(request, question_id):
    return HttpResponse(f'<h1>id: {question_id} </h1>')