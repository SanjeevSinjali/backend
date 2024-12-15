from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


def cv_upload_path(instance, filename):
    print(filename)
    print(instance.email)
    email_part = instance.email.split("@")[0]
    return f"cv/cv_{email_part}.pdf"


class UserModel(AbstractBaseUser, PermissionsMixin):
    JOB_ROLES = [
        ("software_engineer", "Software Engineer"),
        ("frontend_developer", "Frontend Developer"),
        ("qa_engineer", "QA Engineer"),
        ("back_end_developer", "Backend Developer"),
        ("project_manager", "Project Manager"),
        ("full_stack_developer", "Full Stack Developer"),
        ("uiux_designer", "UI/UX Designer"),
        ("graphics_designer", "Graphics Designer"),
        ("laravel_developer", "Laravel Developer"),
        ("digital_marketing", "Digital Marketing"),
        ("php_developer", "PHP Developer"),
        ("flutter_developer", "Flutter Developer"),
    ]

    USER_ROLES = [
        ("admin", "admin"),
        ("seeker", "seeker"),
        ("provider", "provider"),
    ]

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_role = models.CharField(
        max_length=100, choices=JOB_ROLES, blank=True, null=True
    )
    user_role = models.CharField(max_length=100, choices=USER_ROLES, default="seeker")
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    cv = models.FileField(upload_to=cv_upload_path, default=None, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images", default=None, null=True, blank=True
    )
    company = models.ForeignKey(
        "company.CompanyModel",
        on_delete=models.CASCADE,
        null=True,
        related_name="company_users",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # liked_jobs = models.ManyToManyField(
    #     "jobs.JobModel",
    #     related_name="liked_jobs",
    #     blank=True,
    # )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "address", "pincode"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
