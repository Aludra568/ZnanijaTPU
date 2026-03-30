from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:question_id>/', views.question), 
    #int, str(символы кромк "/"), slug(человекочитаемая строка), uuid(набор символов и чисел), path(как str но со "/")
    #можно использовать регулярки( re_path(r"") )
]