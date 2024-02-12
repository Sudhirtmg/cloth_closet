from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from PIL import Image

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class User(AbstractUser):
    is_admin = models.BooleanField('アドミン', default=False)
    is_user = models.BooleanField('ユーザー', default=False)
    is_company = models.BooleanField('会社', default=False)

