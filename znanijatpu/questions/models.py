from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from pytils.translit import translify

# Create your models here.
class Questions(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликованно'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    content = models.TextField(blank=True, verbose_name='Текст вопроса')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Автор', related_name='user_questions')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool (x[0]), x[1]), Status.choices)), 
                                       default=Status.PUBLISHED, verbose_name='Статус')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    image = models.ImageField(upload_to='questions/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение')


    def save(self, *args, **kwargs):
        if not self.slug:  # если slug не задан
            self.slug = slugify(translify(self.title))  # создаем из title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('question', kwargs={'question_slug': self.slug})
    
    def get_absolute_url(self):
        return reverse('questions:question', kwargs={'question_slug': self.slug})
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]


class Faculty(models.Model):
    name = models.CharField(max_length=150, verbose_name='Факультет')
    slug = models.SlugField(unique=True, verbose_name='URL-метка')
    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
    def __str__(self): return self.name

class Program(models.Model):
    name = models.CharField(max_length=100, verbose_name='Форма обучения')
    slug = models.SlugField(unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='programs', verbose_name='Факультет')
    class Meta:
        verbose_name = 'Форма обучения'
        verbose_name_plural = 'Формы обучения'
    def __str__(self): return self.name

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название курса')
    number = models.PositiveSmallIntegerField(verbose_name='Номер курса')
    slug = models.SlugField(unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses', verbose_name='Форма обучения')
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['number']
    def __str__(self): return self.name





class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='categories', verbose_name='Курс')

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'Предметы'

    def save(self, *args, **kwargs):
        if not self.slug:  # если slug не задан
            self.slug = slugify(translify(self.name))  # создаем из title
        super().save(*args, **kwargs)


class Answer(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор ответа')
    content = models.TextField(verbose_name='Текст ответа')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='questions/%Y/%m/%d/', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        ordering = ['time_create']  # Сначала старые ответы
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
    
    def __str__(self):
        return f'Ответ на {self.question.title}'
