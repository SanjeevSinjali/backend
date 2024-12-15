from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from apps.jobs.models import JobModel
from .models import ApplicationModel
from .serializers import ApplicationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class ApplicationViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = ApplicationSerializer

    def list(self, request, *args, **kwargs):
        applications = ApplicationModel.objects.all()
        seralizer = ApplicationSerializer(applications, many=True)
        return Response(seralizer.data)

    def create(self, request, *args, **kwargs):
        applicant = request.user
        if applicant.user_role != "seeker":
            return Response(
                {"error": "You are not authorized to create an application"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        data["applicant"] = applicant.id

        serializer = ApplicationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=["get"], url_path="jobs-with-applicants")
    def get_jobs_with_applicants(self,request):
        jobs = JobModel.objects.prefetch_related("applications")

        response_data = []
        for job in jobs:
            applicants = job.applications.select_related("applicant").values(
                "applicant__id",
                "applicant__email",
                "status",
                "cv",
                "cover_letter",
                "applied_at",
            )
            response_data.append(
                {
                    "job_id": job.id,
                    "job_title": job.title,
                    "applicants": list(applicants),
                    "applicants_count": len(list(applicants))
                }
            )

        return Response(response_data,status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        application = ApplicationModel.objects.get(pk=kwargs.get("pk"))
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        application = ApplicationModel.objects.get(pk=kwargs.get("pk"))
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        application = ApplicationModel.objects.get(pk=kwargs.get("pk"))
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        application = ApplicationModel.objects.get(pk=kwargs.get("pk"))
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
