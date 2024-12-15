from rest_framework.viewsets import ModelViewSet
from .models import CompanyModel
from .serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
