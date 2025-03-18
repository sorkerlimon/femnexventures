from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ServiceCategory, Service, ServiceImage, Order

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'service_type', 'price_per_unit', 'available_stock', 'created_at')
    list_filter = ('category', 'service_type', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ServiceImageInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service__category')
    search_fields = ('user__email', 'service__name', 'notes')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'service')
