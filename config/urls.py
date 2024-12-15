from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import UserViewSet
from apps.jobs.views import JobViewSet
from apps.applications.views import ApplicationViewSet
from apps.company.views import CompanyViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"applications", ApplicationViewSet, basename="applications")
router.register(r"company", CompanyViewSet, basename="company")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
