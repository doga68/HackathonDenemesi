from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.forms import ProfileForm
from .models import Application, Job, Worker

JobForm = modelform_factory(Job, fields=['title', 'description', 'location', 'required_skills'])
WorkerForm = modelform_factory(Worker, fields=['full_name', 'position', 'phone'])


def role_required(role):
    def deco(view):
        @login_required
        @wraps(view)
        def wrapper(request, *a, **kw):
            p = getattr(request.user, 'profile', None)
            if not p or p.role != role:
                return redirect('home')
            return view(request, *a, **kw)
        return wrapper
    return deco


# ---------- İK (işveren) ----------
@role_required('hr')
def hr_dashboard(request):
    jobs = request.user.jobs.annotate(n=Count('applications'))
    return render(request, 'jobs/hr_dashboard.html', {'jobs': jobs, 'workers': request.user.workers.all()})


@role_required('hr')
def job_create(request):
    form = JobForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.employer = request.user
        job.save()
        messages.success(request, 'İlan yayınlandı.')
        return redirect('hr_dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Yeni iş ilanı'})


@role_required('hr')
def applicants(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    apps = job.applications.select_related('applicant__profile')
    rows = sorted(((a, job.match_percent(a.applicant.profile)) for a in apps), key=lambda r: -r[1])
    return render(request, 'jobs/applicants.html', {'job': job, 'rows': rows})


@require_POST
@role_required('hr')
def decide(request, pk, decision):
    app = get_object_or_404(Application, pk=pk, job__employer=request.user)
    if decision in ('accepted', 'rejected'):
        app.status = decision
        app.save()
    return redirect('applicants', pk=app.job_id)


@role_required('hr')
def worker_create(request):
    form = WorkerForm(request.POST or None)
    if form.is_valid():
        w = form.save(commit=False)
        w.employer = request.user
        w.save()
        messages.success(request, 'Çalışan kaydı oluşturuldu.')
        return redirect('hr_dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Yeni çalışan kaydı'})


# ---------- İş arayan ----------
@role_required('seeker')
def job_list(request):
    profile = request.user.profile
    applied = set(request.user.applications.values_list('job_id', flat=True))
    rows = sorted(((j, j.match_percent(profile), j.pk in applied)
                   for j in Job.objects.filter(is_open=True)), key=lambda r: -r[1])
    return render(request, 'jobs/job_list.html', {'rows': rows})


@role_required('seeker')
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_open=True)
    existing = Application.objects.filter(job=job, applicant=request.user).first()
    if request.method == 'POST' and not existing:
        Application.objects.create(job=job, applicant=request.user, message=request.POST.get('message', ''))
        messages.success(request, 'Başvurunuz İK’ya iletildi.')
        return redirect('my_applications')
    return render(request, 'jobs/job_detail.html',
                  {'job': job, 'match': job.match_percent(request.user.profile), 'existing': existing})


@role_required('seeker')
def my_applications(request):
    return render(request, 'jobs/my_applications.html',
                  {'apps': request.user.applications.select_related('job')})


@role_required('seeker')
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profil güncellendi.')
        return redirect('job_list')
    return render(request, 'form.html', {'form': form, 'title': 'Profilim'})
