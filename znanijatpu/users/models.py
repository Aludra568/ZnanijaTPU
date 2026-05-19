# from django.db import models

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
