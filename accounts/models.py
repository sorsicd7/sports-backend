from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import AccountManager
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit() or len(value) != 11 or not value.startswith('09'):
        raise ValidationError('شماره تماس وارد شده نا معتبر است.')
        
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name=' ایمیل')
    username = models.CharField(max_length=30, unique=True, verbose_name='نام کاربری')
    first_name = models.CharField(max_length=30, blank=True,  verbose_name= 'نام')
    last_name = models.CharField(max_length=30, blank=True, verbose_name= 'نام خانوادگی')
    phone_number = models.CharField(max_length=11, validators=[validate_phone_number]\
    , unique=True, blank=True, null=True, verbose_name= '=شماره تماس')   
    description =  models.TextField(blank=True, null=True,  verbose_name= 'توضیحات')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin