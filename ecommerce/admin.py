from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Tenant, User, Product, Customer, Order, OrderItem

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "store_name", "contact_email", "domain")

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (("Extra", {"fields": ("role", "tenant")}),)
    list_display = ("username", "email", "role", "tenant", "is_staff", "is_superuser")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tenant", "price", "stock")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "tenant")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "tenant", "customer", "status", "total_amount", "created_at")
    inlines = [OrderItemInline]
