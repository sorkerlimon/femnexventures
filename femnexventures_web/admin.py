from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, ServiceCategory, Service, ServiceImage, Order

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    readonly_fields = ('id',)
    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'id')
    ordering = ('email',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('id',)
        return self.readonly_fields

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1
    readonly_fields = ('id',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('short_uuid', 'name', 'created_at', 'updated_at')
    search_fields = ('name', 'id')
    list_filter = ('created_at',)
    readonly_fields = ('id',)

    def short_uuid(self, obj):
        return str(obj.id)[:8]
    short_uuid.short_description = 'ID'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('short_uuid', 'name', 'category', 'service_type', 'price_per_unit', 'available_stock', 'created_at')
    list_filter = ('category', 'service_type', 'created_at')
    search_fields = ('name', 'description', 'id')
    readonly_fields = ('id',)
    inlines = [ServiceImageInline]

    def short_uuid(self, obj):
        return str(obj.id)[:8]
    short_uuid.short_description = 'ID'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('short_uuid', 'user', 'service', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service__category')
    search_fields = ('user__email', 'service__name', 'notes', 'id')
    readonly_fields = ('id', 'total_price', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'service')

    def short_uuid(self, obj):
        return format_html('<code>{}</code>', str(obj.id)[:8])
    short_uuid.short_description = 'ID'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields
        return ('id', 'created_at', 'updated_at')
