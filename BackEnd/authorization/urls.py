from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


urlpatterns = [
    # Authorization endpoints
    path("token", TokenObtainPairView.as_view()),
]
