from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'عميل'),
        ('technician', 'فني'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    region = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    
    
    def is_customer(self):
        return self.user_type == 'customer'
        
    def is_technician(self):
        return self.user_type == 'technician'
    
    class Meta:
        db_table = 'auth_user'  # للحفاظ على التوافق مع الجداول القديمة
        
    # حل مشكلة العلاقات ManyToMany
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",
        related_query_name="user",
    )

class InstallationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبول'),
        ('completed', 'مكتمل'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='installation_requests')
    technician = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='technician_requests',
        limit_choices_to={'user_type': 'technician'}
    )
    address = models.TextField()
    region = models.CharField(max_length=100)
    required_power = models.CharField(max_length=50)
    installation_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"طلب تركيب #{self.id} - {self.get_status_display()}"
    
    