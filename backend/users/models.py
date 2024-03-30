from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    picture = models.FileField(_("Profile Picture"), upload_to='profile_pictures/',  blank=True, null=True)
    is_online = models.BooleanField(_("Is Online"), default=False)

    def __str__(self):
        return self.username
