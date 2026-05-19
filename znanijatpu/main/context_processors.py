from questions.models import Category  

def sidebar_data(request):
    """Добавляет категории в каждый шаблон сайта"""
    return {
        'categories': Category.objects.all().order_by('name')
    }