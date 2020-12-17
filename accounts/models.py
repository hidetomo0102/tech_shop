from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager, PermissionsMixin



class UserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('メールアドレス', unique=True)
    first_name = models.CharField('名', max_length=30,)
    last_name = models.CharField('性', max_length=30,)
    tel = models.CharField('電話番号', max_length=30, blank=True)
    address = models.CharField('住所', max_length=100, blank=True)

    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return self.last_name, self.first_name

    def return_username(self):
        return self.email

    def __str__(self):
        return self.email


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True, primary_key=True)
    company_name = models.CharField(max_length=100)

    objects = UserManager()

    class Meta:
        verbose_name = ('Supplier')
        verbose_name_plural = ('Suppliers')

    def __str__(self):
        return self.company_name
