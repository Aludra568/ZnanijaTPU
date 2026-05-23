# users/management/commands/cleanup_codes.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import VerificationCode

class Command(BaseCommand):
    help = 'Удаляет просроченные коды подтверждения из БД'

    def handle(self, *args, **kwargs):
        # Удаляем коды старше 1 часа (с запасом, т.к. код живёт 10 мин)
        expired = VerificationCode.objects.filter(
            created_at__lt=timezone.now() - timezone.timedelta(hours=1)
        )
        count = expired.count()
        expired.delete()
        self.stdout.write(self.style.SUCCESS(f'✅ Удалено {count} просроченных кодов'))