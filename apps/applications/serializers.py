from rest_framework import serializers
from apps.applications.models import ApplicationModel
from apps.users.models import UserModel
from apps.jobs.models import JobModel

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModel
        fields = "__all__"
        write_only_fields = ("cv",)