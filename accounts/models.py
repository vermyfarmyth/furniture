from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])],
    )
    phone = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, default='user')

    def __str__(self):
        return self.user.username
