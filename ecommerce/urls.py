from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (TenantViewSet, ProductViewSet, OrderViewSet, CustomerViewSet,
                    RegisterView, MyTokenObtainPairView)

router = DefaultRouter()
router.register(r"tenants", TenantViewSet, basename="tenant")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", include(router.urls)),
]
