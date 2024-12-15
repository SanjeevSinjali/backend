from apps.company.serializers import CompanySerializer
from apps.company.models import CompanyModel
from .models import JobModel
from rest_framework import serializers


class JobSerializer(serializers.ModelSerializer):
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
        fields = "__all__"
