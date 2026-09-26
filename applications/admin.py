from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'job_title',
        'application_type',
        'location',
        'status',
        'application_date',
    )

    list_filter = (
        'status',
        'application_type',
        'location',
    )

    search_fields = (
        'company_name',
        'job_title',
        'location',
    )