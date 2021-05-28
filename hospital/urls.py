from rest_framework.routers import SimpleRouter
from hospital import views


router = SimpleRouter()

router.register(r'hospital', views.HospitalViewSet)

urlpatterns = router.urls
