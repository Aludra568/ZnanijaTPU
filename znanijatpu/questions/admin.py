from django.contrib import admin
from .models import Questions, Category, Answer, Faculty, Program, Course

# Register your models here.
@admin.register(Questions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'time_create', 'is_published', 'cat')
    list_display_links = ('id', 'title', 'author')
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    prepopulated_fields = {'slug': ('title',),}
    list_per_page = 5


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',),}

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'time_create', 'is_published')

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    prepopulated_fields = {'slug': ('name', 'faculty',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'program')
    list_filter = ('program',)
    prepopulated_fields = {'slug': ('name', 'number',)}



# admin.site.register(Questions, QuestionAdmin)
# admin.site.register(Category)