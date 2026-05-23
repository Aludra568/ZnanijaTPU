from django.contrib import admin
from .models import Question, Subject, Subsubject, Answer

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'is_published', 'subsubject')
    list_display_links = ('id', 'title', 'author')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    prepopulated_fields = {'slug': ('title',),}
    list_per_page = 10


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Subsubject)
class SubsubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    list_filter = ('subject',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'time_create', 'is_published')
    list_filter = ('is_published', 'time_create')
    ordering = ['-time_create']


# @admin.register(Faculty)
# class FacultyAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('name',)}

# @admin.register(Program)
# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('name', 'faculty')
#     prepopulated_fields = {'slug': ('name', 'faculty',)}




# admin.site.register(, QuestionAdmin)
# admin.site.register(Subject)