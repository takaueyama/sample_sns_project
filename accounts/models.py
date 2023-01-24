from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.files.base import ContentFile
from sorl.thumbnail import get_thumbnail, delete
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _

def header_directory_path(instance, filename):
    return 'header/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

def icon_directory_path(instance, filename):
    return 'icon/{}.{}'.format(str(uuid.uuid4()), filename.split('.')[-1])

class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=15,
        unique=True,
        help_text='この項目は必須です。半角英数字、@/./+/-/_ で15文字以下にしてください。',
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    nickname = models.CharField(max_length=50, help_text='この項目は必須です。半角英数字、全角文字、@/./+/-/_ で50文字以下にしてください。')
    user_url = models.URLField(blank=True, max_length=200)
    description = models.TextField(blank=True, max_length=160)
    header_image = models.ImageField(null=True, blank=True, upload_to='header' )
    icon_image = models.ImageField(null=True, blank=True, upload_to='icon')

    REQUIRED_FIELDS = ["nickname"]