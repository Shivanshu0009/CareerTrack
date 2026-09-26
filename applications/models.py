from django.db import models
from django.contrib.auth.models import User

class JobApplication(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='job_applications'
    )

    APPLICATION_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Internship', 'Internship'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
    ]

    STATUS_CHOICES = [
        ('Saved', 'Saved'),
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Assessment', 'Assessment'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    ]

    company_name = models.CharField(max_length=100)

    job_title = models.CharField(max_length=100)

    application_type = models.CharField(
        max_length=20,
        choices=APPLICATION_TYPE_CHOICES
    )

    location = models.CharField(max_length=100)

    application_date = models.DateField()

    deadline = models.DateField(
        null=True,
        blank=True
    )

    job_link = models.URLField(
        blank=True
    )

    salary = models.CharField(
        max_length=50,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Saved'
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"