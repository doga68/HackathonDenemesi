from django.conf import settings
from django.db import models


def parse_skills(text):
    return {s.strip().lower() for s in (text or '').split(',') if s.strip()}


class Profile(models.Model):
    ROLES = [('hr', 'İşveren (İK)'), ('seeker', 'İş Arayan')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)
    company_name = models.CharField('Otel / Şirket adı', max_length=100, blank=True)
    skills = models.CharField('Nitelikler (virgülle ayırın)', max_length=300, blank=True)
    phone = models.CharField('Telefon', max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
