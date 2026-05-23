# test_email.py
import os
import django

# Указываем Django, какой файл настроек использовать
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'znanijatpu.settings')
django.setup()

from django.conf import settings
from django.core.mail import send_mail

print("1. Backend:", settings.EMAIL_BACKEND)
print("2. Host:", settings.EMAIL_HOST)
print("3. User:", settings.EMAIL_HOST_USER)
print("4. Pass length:", len(settings.EMAIL_HOST_PASSWORD or 0))

try:
    send_mail(
        "TEST", 
        "SMTP is working!", 
        settings.DEFAULT_FROM_EMAIL, 
        ["stevesteveonson927@gmail.com"], 
        fail_silently=False
    )
    print("5. SUCCESS: Email sent!")
except Exception as e:
    print("6. ERROR:", e)