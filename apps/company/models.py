from django.db import models


class CompanyModel(models.Model):
    company_name = models.CharField(max_length=50)
    description = models.TextField()
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="company_logo", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employees = models.ManyToManyField(
        "users.UserModel",
        related_name="companies",
        blank=True,
    )
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.company_name
