from rest_framework.routers import DefaultRouter
from subscribers.api.views import SubscribersViewSet

router = DefaultRouter()
router.register('', SubscribersViewSet)

urlpatterns = router.urls
