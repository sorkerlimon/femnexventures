from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the unique identifier
    for authentication instead of username.
    """
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class ServiceCategory(models.Model):
    name = models.CharField(_('category name'), max_length=100, unique=True)
    image = models.ImageField(_('category image'), upload_to="category_images/", blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('service category')
        verbose_name_plural = _('service categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Service(models.Model):
    SERVICE_TYPES = [
        ('account_sale', _('Account Sale')),
        ('boost', _('Boost Service')),
        ('account_creation', _('Account Creation')),
    ]
    
    name = models.CharField(_('service name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    category = models.ForeignKey(
        ServiceCategory, 
        verbose_name=_('category'),
        on_delete=models.CASCADE, 
        related_name="services"
    )
    service_type = models.CharField(
        _('service type'),
        max_length=20, 
        choices=SERVICE_TYPES
    )
    price_per_unit = models.DecimalField(
        _('price per unit'),
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    available_stock = models.IntegerField(
        _('available stock'),
        default=0,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_service_type_display()})"

class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service, 
        verbose_name=_('service'),
        on_delete=models.CASCADE, 
        related_name="images"
    )
    image = models.ImageField(_('image'), upload_to="service_images/")
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('service image')
        verbose_name_plural = _('service images')
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.service.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    user = models.ForeignKey(
        CustomUser, 
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    service = models.ForeignKey(
        Service, 
        verbose_name=_('service'),
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveIntegerField(_('quantity'))
    total_price = models.DecimalField(
        _('total price'),
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        _('status'),
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    notes = models.TextField(_('notes'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.email} - {self.service.name} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        # Calculate total price if not set
        if not self.total_price:
            self.total_price = self.service.price_per_unit * self.quantity
        super().save(*args, **kwargs)
