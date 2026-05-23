from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.home, name='questions_home'),
    # path('<int:question_id>/', views.question_detail), 
    path('create/', views.create, name="create"),
    path('subject/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('subsubject/<slug:subsubject_slug>/', views.subsubject_detail, name='subsubject_detail'),
    path('question/<slug:question_slug>/', views.question_detail, name='question'),
    path('like/<slug:question_slug>/', views.toggle_like, name='toggle_like'),
]    
    # path('faculties/', views.faculty_list, name='faculty_list'),
    # path('faculty/<slug:faculty_slug>/', views.program_list, name='program_list'),
    # path('program/<slug:program_slug>/', views.course_list, name='course_list'),
    # path('course/<slug:course_slug>/', views.category_list, name='category_list'),
    # path('api/cascade/', views.get_cascade_options, name='cascade_api'),


# path('subject/<slug:slug>/', views.questions_by_category, name='questions_by_category')
    #int, str(символы кромк "/"), slug(человекочитаемая строка), uuid(набор символов и чисел), path(как str но со "/")
    #можно использовать регулярки( re_path(r"") )