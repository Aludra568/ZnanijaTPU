from django.db import models

# Create your models here.
class Questions(models.Model):
    topic = models.CharField('Тема', max_length=50)
    title = models.CharField('Заголовок', max_length=250)
    full_teчt = models.TextField('Полный текст')
    date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return self.topic
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'