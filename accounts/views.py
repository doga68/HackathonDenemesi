from django.contrib.auth import login
from django.shortcuts import redirect, render
from .forms import RegisterForm
from .models import Profile


def home(request):
    p = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    if p:
        return redirect('hr_dashboard' if p.role == 'hr' else 'job_list')
    return render(request, 'home.html')


def register(request, role):
    form = RegisterForm(request.POST or None)
    if role == 'hr':
        del form.fields['skills']
    else:
        del form.fields['company_name']
    if form.is_valid():
        user = form.save()
        Profile.objects.create(
            user=user, role=role,
            company_name=form.cleaned_data.get('company_name', ''),
            skills=form.cleaned_data.get('skills', ''))
        login(request, user)
        return redirect('home')
    title = 'İşveren (İK) Kaydı' if role == 'hr' else 'İş Arayan Kaydı'
    return render(request, 'form.html', {'form': form, 'title': title, 'button': 'Kayıt ol'})
