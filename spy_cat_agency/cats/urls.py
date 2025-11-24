from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpyCatViewSet, MissionViewSet, TargetUpdateView

router = DefaultRouter()
router.register(r'spycats', SpyCatViewSet)
router.register(r'missions', MissionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/targets/<int:pk>/', TargetUpdateView.as_view(), name='target-update'),
]
