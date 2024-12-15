from django.db import models
from apps.users.models import UserModel

JOB_TYPES = [
    ("full-time", "Full-time"),
    ("part-time", "Part-time"),
    ("contract", "Contract"),
    ("freelance", "Freelance"),
    ("fresher", "Fresher"),
    ("temporary", "Temporary"),
]

JOB_LEVEL_CHOICES = [
    ("entry", "Entry Level"),
    ("mid", "Mid Level"),
    ("senior", "Senior Level"),
]

SHIFT_CHOICES = [
    ("day", "Day"),
    ("night", "Night"),
    ("flexible", "Flexible"),
]


class JobModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.ForeignKey(
        "company.CompanyModel",
        on_delete=models.CASCADE,
        related_name="jobs",
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    salary = models.CharField(max_length=100, null=True, blank=True)
    required_experience = models.CharField(max_length=50, null=True, blank=True)
    skills_required = models.TextField(null=True, blank=True)
    education_level = models.CharField(max_length=100, null=True, blank=True)
    job_level = models.CharField(
        max_length=20, choices=JOB_LEVEL_CHOICES, default="entry"
    )
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES, default="day")
    posted_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="posted_jobs",
        limit_choices_to={"user_role": "provider"},
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    # applicants = models.ManyToManyField(
    #     UserModel, related_name="applied_jobs", blank=True
    # )
    liked_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class JobsLikedModel(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="job_likes"
    )
    job = models.ForeignKey(JobModel, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "job")
