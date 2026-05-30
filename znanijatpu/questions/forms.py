from .models import Question, Subject, Subsubject, Answer
from django import forms
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea, Select, ClearableFileInput
from django.core.exceptions import ValidationError

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content', 'subsubject', 'image']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок'
            }), 
            "content": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст вопроса',
                'row': 5
            }),
            "subsubject": Select(attrs={
                'class': 'form-control',
            }),
            "image": ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Подсказка в выпадающем списке
    #     self.fields['subject'].empty_label = "Выберите категорию"
    #     # Сортировка категорий по имени (опционально)
    #     self.fields['subject'].queryset = Subject.objects.order_by('name')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['subject'].empty_label = "Сначала выберите курс"
    #     # Изначально скрываем все предметы
    #     self.fields['subject'].queryset = Subject.objects.none()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subsubject'].empty_label = "Выберите предметный курс"
        self.fields['subsubject'].queryset = Subsubject.objects.order_by('name')
        
        # # ✅ ДИНАМИЧЕСКИЙ QUERYSET ДЛЯ ВАЛИДАЦИИ
        # if self.is_bound and 'course_id' in self.data:
        #     try:
        #         course_id = int(self.data.get('course_id'))
        #         self.fields['subsubject'].queryset = Subject.objects.filter(course_id=course_id)
        #     except (ValueError, TypeError):
        #         self.fields['subsubject'].queryset = Subject.objects.none()
        # else:
        #     # При обычной загрузке страницы список пуст
        #     self.fields['subsubject'].queryset = Subject.objects.none()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Ограничение: 5 МБ
            MAX_SIZE = 5 * 1024 * 1024  
            if image.size > MAX_SIZE:
                size_mb = round(image.size / (1024 * 1024), 2)
                raise ValidationError(
                    f'Файл слишком большой. Максимум 5 МБ. Ваш файл: {size_mb} МБ'
                )
            # Проверка типа (защита от загрузки .exe под видом картинки)
            if not image.content_type.startswith('image/'):
                raise ValidationError('Разрешены только изображения (JPG, PNG, WebP и т.д.)')
        return image
    

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content', "image"]  
        widgets = {
            "content": Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Напишите ваш ответ здесь...', 
            }),
            "image": ClearableFileInput(attrs={
                'class': 'form-control',
                # 'accept': 'image/*'  # ← фильтр только для картинок
            })
        }