# from django.db import models
# from apps.users.models import UserModel
# from apps.jobs.models import JobModel


# class ApplicationModel(models.Model):
#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("shortlisted", "Shortlisted"),
#         ("rejected", "Rejected"),
#         ("hired", "Hired"),
#     ]

#     job = models.ForeignKey(
#         JobModel, on_delete=models.CASCADE, related_name="applications"
#     )
#     applicant = models.ForeignKey(
#         UserModel,
#         on_delete=models.CASCADE,
#         related_name="applications",
#         limit_choices_to={"user_role": "seeker"},
#         unique=True,
#     )
#     cv = models.FileField(upload_to="applications/cvs/")
#     cover_letter = models.TextField(null=True, blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
#     applied_at = models.DateTimeField(auto_now_add=True)
#     feedback = models.TextField(null=True, blank=True)
#     interview_scheduled_at = models.DateTimeField(null=True, blank=True)


from django.db import models
from apps.users.models import UserModel
from apps.jobs.models import JobModel


class ApplicationModel(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"
        HIRED = "hired", "Hired"

    job = models.ForeignKey(
        JobModel, on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="applicants",
        limit_choices_to={"user_role": "seeker"},
    )
    cv = models.FileField(upload_to="applications/cvs/%Y/%m/%d/")
    cover_letter = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING
    )
    applied_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(null=True, blank=True)
    interview_scheduled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        constraints = [
            models.UniqueConstraint(
                fields=["job", "applicant"], name="unique_application_per_job"
            )
        ]

    def __str__(self):
        return f"{self.applicant} - {self.job} ({self.status})"
