import uuid
from django.contrib.auth.models import  AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from .custom_user import Role, CustomUserManager
# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        
    )
    email = models.EmailField(unique=True)
    firstname = models.CharField(
        max_length = 25,
        null = False)
    lastname = models.CharField(
        max_length = 25,
        null = False)
    role = models.CharField(
        max_length = 20,
        choices = Role.choices,
        default = Role.CUSTOMER
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    datejoined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Categories(models.Model):
    category_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
    )
    name = models.CharField(
        max_length = 50,
        null = False
    )
    slug = models.CharField(
        max_length = 60,
        null = False
    )
    parent_id = models.ForeignKey(
        'self',
        on_delete = models.CASCADE,
        related_name = "subcategories",
        null = True,
        blank = True
    )

class Product(models.Model):
    product_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        db_index = True
    )
    product_name = models.CharField(
        max_length = 50,
        null = False
    )
    slug = models.CharField(
        max_length = 50,
        null = False
    )
    description = models.TextField(
        null = False
    )
    price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2
    )
    in_stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Categories,
        on_delete = models.CASCADE,
        related_name = "products"
    )

    seller = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = "products"
    )
    
