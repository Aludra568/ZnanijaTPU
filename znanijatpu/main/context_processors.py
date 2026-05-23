from questions.models import Subject

def sidebar_context(request):
    # Передаём предметы в контекст каждого шаблона
    return {'subjects': Subject.objects.all().order_by('name')}