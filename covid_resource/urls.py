from rest_framework.routers import SimpleRouter
from covid_resource import views


router = SimpleRouter()

router.register(r'rest_framework', views.ResourceViewSet)

urlpatterns = router.urls
