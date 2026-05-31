from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Question, Subject, Subsubject, Answer, Like
from .forms import QuestionForm, AnswerForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from pytils.translit import translify  # Для корректной кириллицы в slug
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count, Q

# Create your views here.
def index(request):
    return render(request, 'questions/index.html')

def news_home(request):
    questions = Question.objects.all()
    return render(request, 'questions/questions_home.html', {'questions': questions})

class NewUpdateView(UpdateView):
    model = Question
    template_name = 'questions/create.html'
    form_class = QuestionForm

class NewDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('questions:questions_home')  # ← надёжнее
    template_name = 'questions/news-delete.html'

@login_required
def create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            
            # Генерация slug с поддержкой кириллицы
            if not question.slug and question.title:
                question.slug = slugify(translify(question.title)) or f"q-{question.id}"
                
            question.save()
            return redirect('home')  # Используем имя URL, а не '/'
    else:
        form = QuestionForm()

    return render(request, 'questions/create.html', {
        'form': form,
        'subjects': Subject.objects.all(),  # Передаём предметы для формы
    })

def home(request):
    questions = Question.objects.filter(is_published=True) \
        .select_related('subsubject__subject', 'author') \
        .order_by('-time_create')
    
    return render(request, 'main/index.html', {
        'questions': questions,
    })

def category(request, cat_slug):
    subject = get_object_or_404(Subject, slug=cat_slug)
    
    questions = Question.objects.filter(
        subsubject__subject=subject, 
        is_published=True
    ).select_related('author', 'subsubject')

    subjects = Subject.objects.all()
    
    return render(request, 'main/category.html', {
        'questions': questions,
        'category': subject,
        'categories': subjects,  
    })

def subject_detail(request, subject_slug):
    """Показывает список подпредметов выбранного предмета"""
    subject = get_object_or_404(Subject, slug=subject_slug)
    subsubjects = subject.subsubjects.all()  # related_name='subsubjects' из модели
    
    return render(request, 'questions/subject_detail.html', {
        'subject': subject,
        'subsubjects': subsubjects,
    })

def subsubject_detail(request, subsubject_slug):
    subsubject = get_object_or_404(Subsubject, slug=subsubject_slug)
    
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list('question_id', flat=True))

    questions = Question.objects.filter(
        subsubject=subsubject, 
        is_published=True
    ).select_related('author').annotate(
        likes_count=Count('likes'),
        answers_count=Count('answers')  # ← ДОБАВЛЕНО
    ).order_by('-time_create')
    
    return render(request, 'questions/subsubject_detail.html', {
        'subsubject': subsubject,
        'questions': questions,
        'liked_ids': liked_ids,
    })

def question_detail(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug)
    answers = Answer.objects.filter(question=question, is_published=True)
    
    if request.method == 'POST':
        if request.user.is_authenticated:  
            form = AnswerForm(request.POST, request.FILES)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question = question
                answer.author = request.user
                answer.save()
                return redirect('questions:question', question_slug=question.slug)
        else:
            return redirect('users:login')  
    else:
        form = AnswerForm()

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })


@login_required
def toggle_like(request, question_slug): 
    if request.method == 'POST':
        question = get_object_or_404(Question, slug=question_slug)
        like, created = Like.objects.get_or_create(user=request.user, question=question)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': question.likes.count()
        })
    return JsonResponse({'success': False}, status=400)




def search_questions(request):
    query = request.GET.get('q', '').strip()
    
    # Получаем ID лайков текущего пользователя (для синхронизации с карточками)
    liked_ids = set()
    if request.user.is_authenticated:
        liked_ids = set(Like.objects.filter(user=request.user).values_list('question_id', flat=True))

    if query:
        # Поиск по заголовку ИЛИ тексту вопроса (без учёта регистра)
        questions = Question.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).select_related('author', 'subsubject__subject').annotate(
            likes_count=Count('likes'),
            answers_count=Count('answers')
        ).order_by('-time_create')
    else:
        questions = Question.objects.none()

    return render(request, 'questions/search_results.html', {
        'questions': questions,
        'query': query,
        'liked_ids': liked_ids,
    })
#  УДАЛЕНЫ: faculty_list, program_list, course_list, category_list, subject_questions, get_cascade_options
# Эти функции вызовут NameError, так как модели Faculty/Program/Course закомментированы в models.py