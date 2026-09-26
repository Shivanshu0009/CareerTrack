from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout

@login_required
def home(request):

    applications = JobApplication.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_applications = applications.count()

    saved = applications.filter(status='Saved').count()

    applied = applications.filter(status='Applied').count()

    under_review = applications.filter(status='Under Review').count()

    assessments = applications.filter(status='Assessment').count()

    interviews = applications.filter(status='Interview').count()

    selected = applications.filter(status='Selected').count()

    rejected = applications.filter(status='Rejected').count()

    active_applications = (
        applied
        + under_review
        + assessments
        + interviews
    )

    context = {
        'applications': applications,
        'total_applications': total_applications,
        'saved': saved,
        'applied': applied,
        'under_review': under_review,
        'assessments': assessments,
        'interviews': interviews,
        'selected': selected,
        'rejected': rejected,
        'active_applications': active_applications,
    }

    return render(request, 'home.html', context)

@login_required
def add_application(request):

    if request.method == 'POST':

        form = JobApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)

            application.user = request.user

            application.save()

            return redirect('home')

    else:

        form = JobApplicationForm()

    return render(
        request,
        'add_application.html',
        {'form': form}
    )


@login_required
def edit_application(request, application_id):

    application = get_object_or_404(
      JobApplication,
      id=application_id,
      user=request.user
    )

    if request.method == 'POST':

        form = JobApplicationForm(
            request.POST,
            instance=application
        )

        if form.is_valid():

            form.save()

            return redirect('home')

    else:

        form = JobApplicationForm(
            instance=application
        )

    return render(
        request,
        'edit_application.html',
        {
            'form': form,
            'application': application
        }
    )


@login_required
def delete_application(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    if request.method == 'POST':

        application.delete()

        return redirect('home')

    return render(
        request,
        'delete_application.html',
        {
            'application': application
        }
    )


@login_required
def application_list(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )


    # Search

    search = request.GET.get('search', '')

    if search:

        applications = applications.filter(
            company_name__icontains=search
        ) | applications.filter(
            job_title__icontains=search
        )


    # Status filter

    status = request.GET.get('status', '')

    if status:

        applications = applications.filter(
            status=status
        )


    # Application type filter

    application_type = request.GET.get(
        'application_type',
        ''
    )

    if application_type:

        applications = applications.filter(
            application_type=application_type
        )


    # Sorting

    sort = request.GET.get(
        'sort',
        'newest'
    )


    if sort == 'oldest':

        applications = applications.order_by(
            'created_at'
        )

    elif sort == 'company':

        applications = applications.order_by(
            'company_name'
        )

    elif sort == 'application_date':

        applications = applications.order_by(
            '-application_date'
        )

    elif sort == 'status':

        applications = applications.order_by(
            'status'
        )

    else:

        applications = applications.order_by(
            '-created_at'
        )


    context = {

        'applications': applications,

        'search': search,

        'selected_status': status,

        'selected_type': application_type,

        'selected_sort': sort,

        'status_choices':
            JobApplication.STATUS_CHOICES,

        'application_type_choices':
            JobApplication.APPLICATION_TYPE_CHOICES,

    }


    return render(
        request,
        'application_list.html',
        context
    )

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect('home')

    else:

        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )

def logout_view(request):

    logout(request)

    return redirect('login')

@login_required
def analytics(request):

    applications = JobApplication.objects.filter(
        user=request.user
    )

    total = applications.count()

    saved = applications.filter(status='Saved').count()

    applied = applications.filter(status='Applied').count()

    under_review = applications.filter(
        status='Under Review'
    ).count()

    assessments = applications.filter(
        status='Assessment'
    ).count()

    interviews = applications.filter(
        status='Interview'
    ).count()

    selected = applications.filter(
        status='Selected'
    ).count()

    rejected = applications.filter(
        status='Rejected'
    ).count()

    full_time = applications.filter(
        application_type='Full-time'
    ).count()

    internship = applications.filter(
        application_type='Internship'
    ).count()

    part_time = applications.filter(
        application_type='Part-time'
    ).count()

    contract = applications.filter(
        application_type='Contract'
    ).count()

    # Calculate percentages

    if total > 0:

        saved_percent = round((saved / total) * 100)

        applied_percent = round((applied / total) * 100)

        review_percent = round(
            (under_review / total) * 100
        )

        assessment_percent = round(
            (assessments / total) * 100
        )

        interview_percent = round(
            (interviews / total) * 100
        )

        selected_percent = round(
            (selected / total) * 100
        )

        rejected_percent = round(
            (rejected / total) * 100
        )

    else:

        saved_percent = 0
        applied_percent = 0
        review_percent = 0
        assessment_percent = 0
        interview_percent = 0
        selected_percent = 0
        rejected_percent = 0

    context = {

        'total': total,

        'saved': saved,
        'applied': applied,
        'under_review': under_review,
        'assessments': assessments,
        'interviews': interviews,
        'selected': selected,
        'rejected': rejected,

        'full_time': full_time,
        'internship': internship,
        'part_time': part_time,
        'contract': contract,

        'saved_percent': saved_percent,
        'applied_percent': applied_percent,
        'review_percent': review_percent,
        'assessment_percent': assessment_percent,
        'interview_percent': interview_percent,
        'selected_percent': selected_percent,
        'rejected_percent': rejected_percent,
    }

    return render(
        request,
        'analytics.html',
        context
    )

@login_required
def application_detail(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    return render(
    request,
    'application_detail.html',
    {
        'application': application,
        'status_choices': JobApplication.STATUS_CHOICES
    }
   ) 

@login_required
def update_status(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id,
        user=request.user
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            choice[0]
            for choice in JobApplication.STATUS_CHOICES
        ]

        if new_status in valid_statuses:

            application.status = new_status

            application.save()

    return redirect(
        'application_detail',
        application_id=application.id
    )