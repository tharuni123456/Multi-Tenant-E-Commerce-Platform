from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Tenant, Product, Customer, Order
from .serializers import (TenantSerializer, ProductSerializer, CustomerSerializer,
                          OrderSerializer, UserRegisterSerializer)
from .permissions import TenantSafe, IsStoreOwner, IsStaff
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import MyTokenObtainPairSerializer

User = get_user_model()

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, TenantSafe]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.tenant:
            return Product.objects.filter(tenant=user.tenant)
        return Product.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role not in ['owner', 'staff']:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You do not have permission to create a product")
        serializer.save(tenant=self.request.user.tenant)

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, TenantSafe]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.tenant:
            return Customer.objects.filter(tenant=user.tenant)
        return Customer.objects.none()

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, TenantSafe]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.tenant:
            if user.role == 'customer':
                # if customers: show only their placed orders (if linked)
                return Order.objects.filter(tenant=user.tenant, placed_by=user)
            # owner/staff: see all orders for tenant
            return Order.objects.filter(tenant=user.tenant)
        return Order.objects.none()

    def perform_create(self, serializer):
        # only customers place orders in this design
        if self.request.user.role != 'customer':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only customers can place orders")
        serializer.save()
