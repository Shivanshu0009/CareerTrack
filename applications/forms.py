from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            'company_name',
            'job_title',
            'application_type',
            'location',
            'application_date',
            'deadline',
            'job_link',
            'salary',
            'status',
            'notes',
        ]

        widgets = {
            'application_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'deadline': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'notes': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Add any notes about this application...'
                }
            ),
        }