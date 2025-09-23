import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(
        max_length = 25,
        null = False)
    lastname = models.CharField(
        max_length = 25,
        null = False)
    password = models.CharField(
        max_length = 250,
        null = False)
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
    
