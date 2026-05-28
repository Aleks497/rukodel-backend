from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Master, Product, Order, OrderItem, Cart, Review


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets     = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Дополнительно', {'fields': ('role', 'phone', 'email')}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display       = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display  = ['user', 'specialty', 'rating']
    search_fields = ['user__username', 'specialty']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'master', 'category', 'price', 'quantity', 'is_active']
    list_filter   = ['category', 'is_active']
    search_fields = ['name']
    list_editable = ['price', 'quantity', 'is_active']


class OrderItemInline(admin.TabularInline):
    model      = OrderItem
    extra      = 0
    can_delete = False
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter   = ['status']
    list_editable = ['status']
    inlines       = [OrderItemInline]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
