# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .serializers import JobSerializer
from .models import JobModel, JobsLikedModel
from rest_framework.response import Response
from rest_framework import status
from apps.users.models import UserModel
from rest_framework.decorators import action
from django.db import models
from datetime import datetime, timedelta


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def list(self, request, *args, **kwargs):
        jobs = JobModel.objects.all()

        location = request.query_params.get("location", None)
        job_type = request.query_params.get("job_type", None)
        salary_range = request.query_params.get("salary_range", None)
        required_experience = request.query_params.get("required_experience", None)
        education_level = request.query_params.get("education_level", None)
        job_level = request.query_params.get("job_level", None)
        shift = request.query_params.get("shift", None)
        title = request.query_params.get("title", None)
        posted_by = request.query_params.get("posted_by", None)
        deadline = request.query_params.get("deadline", None)

        if posted_by:
            jobs = jobs.filter(posted_by=posted_by)
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if salary_range:
            jobs = jobs.filter(salary_range__icontains=salary_range)
        if required_experience:
            jobs = jobs.filter(required_experience__icontains=required_experience)
        if education_level:
            jobs = jobs.filter(education_level__icontains=education_level)
        if job_level:
            jobs = jobs.filter(job_level=job_level)
        if shift:
            jobs = jobs.filter(shift=shift)
        if title:
            jobs = jobs.filter(title__icontains=title)

        now = datetime.now()

        if deadline == "day":
            start_date = now
            end_date = now + timedelta(days=1)
            jobs = jobs.filter(
                application_deadline__gte=start_date, application_deadline__lte=end_date
            )
        elif deadline == "week":
            start_date = now
            end_date = now + timedelta(weeks=1)
            jobs = jobs.filter(
                application_deadline__gte=start_date, application_deadline__lte=end_date
            )
        elif deadline == "month":
            start_date = now
            end_date = now + timedelta(days=30)
            jobs = jobs.filter(
                application_deadline__gte=start_date, application_deadline__lte=end_date
            )

        seralizer = JobSerializer(jobs, many=True)
        return Response(seralizer.data)

    @action(detail=False, methods=["get"], url_path="search-job-count")
    def search_job_count(self, request, *args, **kwargs):
        jobs = JobModel.objects.all()
        job_counts = (
            jobs.values("title")
            .annotate(count=models.Count("title"))
            .order_by("-count")
        )

        response_data = [
            {"title": job["title"], "count": job["count"]} for job in job_counts
        ]

        return Response(response_data, status=status.HTTP_200_OK)

    from django.http import JsonResponse

    @action(detail=False, methods=["get"], url_path="popular-job")
    def popular_jobs(self, request):
        """
        Returns a list of popular jobs sorted by liked_count in descending order.
        """
        popular_jobs = JobModel.objects.filter(is_active=True).order_by("-liked_count")[
            :8
        ]
        jobs_data = [
            {
                "id": job.id,
                "title": job.title,
                "liked_count": job.liked_count,
                "company_name": job.company.company_name,
                "company_logo": job.company.logo,
            }
            for job in popular_jobs
        ]
        return Response({"popular_jobs": jobs_data})

    @action(detail=False, methods=["post"], url_path="like-job")
    def like_job(self, request):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'error': 'Authentication required'}, status=401)
        job_id = request.data.get("job_id")

        job = JobModel.objects.get(pk=job_id)
        job_like, created = JobsLikedModel.objects.get_or_create(
            user=request.user, job=job
        )

        if created:
            # Increment count only if the user has not already liked the job
            job.liked_count += 1
            job.save()
            return Response(
                {"message": "Job liked", "liked_count": job.liked_count},
                status=status.HTTP_201_CREATED,
            )
        else:
            # If the user already liked, remove the like and decrement liked_count
            job_like.delete()
            job.liked_count -= 1
            job.save()
            return Response(
                {"message": "Job unliked", "liked_count": job.liked_count},
                status=status.HTTP_200_OK,
            )

    def create(self, request, *args, **kwargs):
        # user = UserModel.objects.get(pk=request.data.get("posted_by"))
        user = request.user
        if user.user_role != "provider":
            return Response(
                {"error": "You are not authorized to create a job"},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Check if the user has a company, if so, set the company for the job
        if user.company:
            request.data["company_id"] = user.company.id
        # else:
        #     request.data["company_id"] = (
        #         None  # Leave company as null if user doesn't have one
        #     )
        data = request.data.copy()
        data["posted_by"] = user.id
        print(data)

        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        job = JobModel.objects.get(pk=kwargs.get("pk"))
        serializer = JobSerializer(job)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        job = JobModel.objects.get(pk=kwargs.get("pk"))
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        job = JobModel.objects.get(pk=kwargs.get("pk"))
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        job = JobModel.objects.get(pk=kwargs.get("pk"))
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
