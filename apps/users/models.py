from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("The Email field must be set")
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)

    #     if password:
    #         user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault(
            "is_active", True
        )  # Ensure is_active is True by default
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault("is_staff", True)
    #     extra_fields.setdefault("is_superuser", True)
    #     extra_fields.setdefault("user_role", "admin")

    #     if extra_fields.get("is_staff") is not True:
    #         raise ValueError("Superuser must have is_staff=True.")
    #     if extra_fields.get("is_superuser") is not True:
    #         raise ValueError("Superuser must have is_superuser=True.")

    #     return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault(
            "is_active", True
        )  # Explicitly set is_active for superusers
        extra_fields.setdefault("user_role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# def cv_upload_path(instance, filename):
#     print(filename)
#     print(instance.email)
#     email_part = instance.email.split("@")[0]
#     return f"cv/cv_{email_part}.pdf"


class UserModel(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = [
        ("admin", "admin"),
        ("seeker", "seeker"),
        ("provider", "provider"),
    ]

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_role = models.CharField(max_length=100, blank=True, null=True)
    user_role = models.CharField(max_length=100, choices=USER_ROLES, default="seeker")
    address = models.CharField(max_length=100)
    skills = models.CharField(max_length=100, blank=True, null=True)
    # cv = models.FileField(upload_to=cv_upload_path, default=None, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images", default=None, null=True, blank=True
    )
    company = models.ForeignKey(
        "company.CompanyModel",
        on_delete=models.CASCADE,
        null=True,
        related_name="company_users",
    )
    experience = models.IntegerField(blank=True, null=True)
    pincode = models.CharField(max_length=100)
    # experience = models.IntegerField(blank=True, null=True)
    # pincode = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "address", "pincode"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def get_full_name(self):
    #     return f"{self.first_name} {self.last_name}"

    # def get_short_name(self):
    #     return self.first_name

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         old_user = UserModel.objects.filter(pk=self.pk).first()
    #         if old_user and old_user.password != self.password:
    #             self.set_password(self.password)
    #     else:
    #         if self.password:
    #             self.set_password(self.password)

    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if (
            not self.pk
        ):  # If the user is being created (i.e., no primary key exists yet)
            self.is_active = True  # Ensure is_active is set to True by default

        if self.pk:  # If the user is being updated
            old_user = UserModel.objects.filter(pk=self.pk).first()
            if old_user and old_user.password != self.password:
                self.set_password(self.password)
        else:  # If the user is being created
            if self.password:
                self.set_password(self.password)

        super().save(*args, **kwargs)
