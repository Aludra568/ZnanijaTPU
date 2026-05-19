from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Questions, Category, Answer, Faculty, Program, Course
from .forms import QuestionsForm, AnswerForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.text import slugify


# Create your views here.
def index(request):
    return render(request, 'questions/index.html')

# def show_question(request, question_id):
#     return HttpResponse(f'<h1>id: {question_id} </h1>')

def news_home(request):
    questions = Questions.objects.all() #получение значений из данной таблицы
    return render(request, 'questions/questions_home.html', {'questions': questions})


# class NewDetailView(DetailView):
#     model = Questions
#     template_name = 'questions/question_detail.html'
#     context_object_name = 'question'
#     slug_url_kwarg = 'question_slug'


class NewUpdateView(UpdateView):
    model = Questions
    template_name = 'questions/create.html'

    form_class = QuestionsForm


class NewDeleteView(DeleteView):
    model = Questions
    success_url = '/questions/'
    template_name = 'questions/news-delete.html'

@login_required
def create(request):
    # error = ''
    if request.method == "POST":
        form = QuestionsForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
                        
            # if not question.slug and question.title:
            #     slug = slugify(question.title)
            #     if not slug:
            #         slug = f"vopros-{question.id}"  
            #     question.slug = slug
            
            question.save()
            return redirect('/')
    else:
            # error = 'Форма была неверной'
        form = QuestionsForm()

    # data = {
    #     'form': form,
    #     'error': error
    # }

    return render(request, 'questions/create.html', {
        'form': form,
        'faculties': Faculty.objects.all(),
        })


def home(request):
    questions = Questions.objects.filter(is_published=True
        ).select_related('cat', 'author').order_by('-time_create')
      # только опубликованные
    # categories = Category.objects.all()  # все категории
    
    return render(request, 'main/index.html', {  # ← правильный путь к шаблону
        'questions': questions,
        # 'categories': categories,  # ← передаём в шаблон
    })

def category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    
    questions = Questions.objects.filter(cat=category, is_published=True)

    categories = Category.objects.all()
    
    return render(request, 'main/category.html', {  # ← создай этот шаблон
        'questions': questions,
        'category': category,
        'categories': categories,  
    })

def question_detail(request, question_slug):
    question = get_object_or_404(Questions, slug=question_slug)
    answers = Answer.objects.filter(question=question, is_published=True)
    # Обработка формы ответа
    if request.method == 'POST':
        if request.user.is_authenticated:  
        
            form = AnswerForm(request.POST, request.FILES)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question = question
                answer.author = request.user
                answer.save()
                return redirect('questions:question', question_slug=question.slug)  # Перезагрузка страницы
        else:
            return redirect('users:login')  
    else:
        form = AnswerForm()

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })




def faculty_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'questions/hierarchy.html', {
        'faculties': faculties, 'level': 'faculty'
    })

def program_list(request, faculty_slug):
    faculty = get_object_or_404(Faculty, slug=faculty_slug)
    programs = faculty.programs.all()
    return render(request, 'questions/hierarchy.html', {
        'faculty': faculty, 'programs': programs, 'level': 'program'
    })

def course_list(request, program_slug):
    program = get_object_or_404(Program, slug=program_slug)
    courses = program.courses.all()
    return render(request, 'questions/hierarchy.html', {
        'program': program, 'courses': courses, 'level': 'course'
    })

def category_list(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    categories = course.categories.all()
    return render(request, 'questions/hierarchy.html', {
        'course': course, 'categories': categories, 'level': 'category'
    })

# Страница с вопросами конкретного предмета
def subject_questions(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    questions = Questions.objects.filter(cat=category, is_published=True).select_related('author')
    return render(request, 'questions/category_questions.html', {
        'category': category, 'questions': questions
    })



def get_cascade_options(request):
    """Возвращает JSON для зависимых списков"""
    faculty_id = request.GET.get('faculty_id')
    program_id = request.GET.get('program_id')
    course_id = request.GET.get('course_id')

    if faculty_id:
        data = list(Program.objects.filter(faculty_id=faculty_id).values('id', 'name'))
    elif program_id:
        data = list(Course.objects.filter(program_id=program_id).values('id', 'name'))
    elif course_id:
        data = list(Category.objects.filter(course_id=course_id).values('id', 'name'))
    else:
        data = []
        
    return JsonResponse(data, safe=False)