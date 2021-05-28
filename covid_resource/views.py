from rest_framework.viewsets import ModelViewSet
from covid_resource.models import Resource
from covid_resource.serializers import ResourceSerializer


class ResourceViewSet(ModelViewSet):
    queryset = Resource.objects.order_by('resource_type')
    serializer_class = ResourceSerializer
