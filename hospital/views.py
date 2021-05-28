from rest_framework.viewsets import ModelViewSet
from hospital.serializers import HospitalSerializer
from hospital.models import Hospital


class HospitalViewSet(ModelViewSet):
    queryset = Hospital.objects.order_by('pk')
    serializer_class = HospitalSerializer
