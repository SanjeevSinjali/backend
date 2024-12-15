from .views import CompanyView, CompanyDetailView
from django.urls import path

urlpatterns = [
    path("", CompanyView.as_view(), name="company"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company-detail"),
]
