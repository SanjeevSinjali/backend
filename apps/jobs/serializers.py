from apps.company.serializers import CompanySerializer
from apps.company.models import CompanyModel
from apps.applications.serializers import ApplicationSerializer
from .models import JobModel
from rest_framework import serializers


class JobSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True)
    company = CompanySerializer(
        read_only=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=CompanyModel.objects.all(),
        source="company",
        write_only=True,
        required=False,
    )

    class Meta:
        model = JobModel
        fields = [
            "id",
            "title",
            "description",
            "company_id",
            "company",
            "location",
            "job_type",
            "salary",
            "required_experience",
            "skills_required",
            "education_level",
            "job_level",
            "shift",
            "posted_by",
            "posted_at",
            "application_deadline",
            "is_active",
            "liked_count",
            "applications", 
        ]
