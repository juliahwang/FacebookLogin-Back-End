from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models

# Create your models here.


class UserManager(DjangoUserManager):
    def create_facebook_user(self, user_info):
        return self.create_user(
            username=user_info['id'],
            first_name=user_info['first_name', ''],
            last_name=user_info['last_name', ''],
            user_types=User.USER_TYPE_FACEBOOK
        )

class User(AbstractUser):
    USER_TYPE_DJANGO = 'django'
    USER_TYPE_FACEBOOK = 'facebook'
    CHOICES_USER_TYPE = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    pass
