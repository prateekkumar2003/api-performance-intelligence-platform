from django.urls import path
from .views import HealthCheckView, DummyAPIView, SlowAPIView

urlpatterns = [
    path("health/", HealthCheckView.as_view()),
    path("dummy/", DummyAPIView.as_view()),
    path("slow/", SlowAPIView.as_view()),
]