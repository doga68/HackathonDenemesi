from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from accounts.models import Profile
from jobs.models import Job, Worker

PW = 'Demo12345!'


class Command(BaseCommand):
    help = 'Demo verisi yükler'

    def handle(self, *args, **kw):
        hr, new = User.objects.get_or_create(username='otel_hr', defaults={'first_name': 'Ayşe', 'last_name': 'Yıldız'})
        if new:
            hr.set_password(PW); hr.save()
            Profile.objects.create(user=hr, role='hr', company_name='Kyrenia Palace Hotel')
            for t, d, s in [
                ('Garson', 'Restoran servisi için ekip arkadaşı.', 'garson, ingilizce, takım çalışması'),
                ('Resepsiyonist', 'Ön büro karşılama ve rezervasyon.', 'resepsiyon, ingilizce, almanca, opera'),
                ('Kat Görevlisi', 'Oda temizliği ve düzeni.', 'temizlik, kat hizmetleri'),
            ]:
                Job.objects.create(employer=hr, title=t, description=d, location='Girne', required_skills=s)
            Worker.objects.create(employer=hr, full_name='Mehmet Kaya', position='Aşçıbaşı', phone='0533 000 00 00')
        for u, skills in [('aday1', 'garson, ingilizce'), ('aday2', 'resepsiyon, ingilizce, almanca')]:
            user, new = User.objects.get_or_create(username=u)
            if new:
                user.set_password(PW); user.save()
                Profile.objects.create(user=user, role='seeker', skills=skills)
        self.stdout.write('Demo verisi hazır. Şifre: ' + PW)
