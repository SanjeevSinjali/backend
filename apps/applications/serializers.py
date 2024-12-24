from rest_framework import serializers
from apps.applications.models import ApplicationModel
from apps.users.models import UserModel
from apps.jobs.models import JobModel
from apps.users.serializers import UserSerializer
from apps.company.models import CompanyModel


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = [
            "company_name",
        ]


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = JobModel
        fields = [
            "id",
            "company",
            "title",
            "salary",
            "location",
            "description",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    # applicant = UserSerializer()
    # job = JobSerializer(read_only=True)  # Nest JobSerializer for job details
    # applicant = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    job = serializers.PrimaryKeyRelatedField(
        queryset=JobModel.objects.all()
    )  # Accept job ID on POST
    applicant = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())
    job_details = JobSerializer(
        source="job", read_only=True
    )  # Include nested job details on GET

    class Meta:
        model = ApplicationModel
        fields = "__all__"
        write_only_fields = ("cv",)
        extra_kwargs = {
            "job_details": {"read_only": True},
        }
