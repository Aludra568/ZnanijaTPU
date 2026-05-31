from django.db import models
from django.utils import timezone
from datetime import timedelta

class VerificationCode(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    code = models.CharField(max_length=6, verbose_name='Код')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    @property
    def is_expired(self):
        # return (timezone.now() - self.created_at).total_seconds() > 600
        return timezone.now() > self.created_at + timedelta(minutes=10)


    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    def __str__(self):
        return f'Код для {self.email}'
# # Create your models here.
# from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.utils.html import strip_tags

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, first_name, last_name, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Поле email должно быть заполненно.")
#         email = self.normalize_email(email)
#         user = self.model(email=email, first_name=first_name, last_name = last_name, **extra_fields)
#         user.set_password(password)
#         user.save(using=self.db)

#     def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
#         extra_fields.setdefault('')

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True, max_length=254)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
