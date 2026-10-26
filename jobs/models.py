from django.conf import settings
from django.db import models
from accounts.models import parse_skills

User = settings.AUTH_USER_MODEL


class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField('Pozisyon', max_length=100)
    description = models.TextField('Açıklama')
    location = models.CharField('Konum', max_length=100, blank=True)
    required_skills = models.CharField('Aranan nitelikler (virgülle ayırın)', max_length=300)
    is_open = models.BooleanField('Açık', default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def match_percent(self, profile):
        req = parse_skills(self.required_skills)
        if not req:
            return 0
        return round(100 * len(req & parse_skills(profile.skills)) / len(req))


class Application(models.Model):
    STATUS = [('pending', 'Beklemede'), ('accepted', 'Kabul edildi'), ('rejected', 'Reddedildi')]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField('Ön yazı', blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-created_at']


class Worker(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workers')
    full_name = models.CharField('Ad Soyad', max_length=100)
    position = models.CharField('Pozisyon', max_length=100)
    phone = models.CharField('Telefon', max_length=30, blank=True)

    def __str__(self):
        return self.full_name
