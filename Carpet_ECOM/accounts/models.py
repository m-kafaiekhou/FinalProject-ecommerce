from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from core.utils import phone_regex_validator


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    phone_number = models.CharField(max_length=13, unique=True,
                                    validators=[phone_regex_validator],
                                    verbose_name=_('Phone Number'),
                                    error_messages={
                                        "unique": _("A Customer with that Phone number already exists."),
                                    },
                                    )
    first_name = models.CharField(max_length=30, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=30, verbose_name=_('Last Name'))
    picture = models.ImageField(upload_to='customer/pic', null=True, blank=True)

    is_active = models.BooleanField(default=True, verbose_name=_('Activation Status'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff Status'))
    is_superuser = models.BooleanField(default=False, verbose_name=_('Superuser Status'))

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.phone_number

    def save(self, *args, **kwargs):
        self.phone_number = '0' + self.phone_number[3:] if len(self.phone_number) == 13 else self.phone_number
        super(CustomUser, self).save(*args, **kwargs)

    def role(self):
        return "Super User" if self.is_superuser else self.groups.get()

    role.short_description = _('Role')
        