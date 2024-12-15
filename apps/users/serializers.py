from apps.company.models import CompanyModel
from apps.company.serializers import CompanySerializer
from .models import UserModel
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
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
        model = UserModel
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}, "cv": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        user.is_active = True
        if password:
            user.set_password(password)
            user.save()

        return user
