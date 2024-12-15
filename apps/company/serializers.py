from .models import CompanyModel
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = "__all__"
