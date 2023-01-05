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
        # help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
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


    # def save(self, *args, **kwargs):
    #     super(CustomUser, self).save(*args, **kwargs)
    #     if self.header_image:
    #         new_width = 300
    #         new_height = 300
    #         if self.header_image.width > 1500 or self.header_image.height > 500:
    #             resized = get_thumbnail(self.header_image, "{}x{}".format(new_width, new_height))
    #             # name = resized.name.split('/')[-1]
    #             self.header_image.save(self.header_image.name.split('/')[-1], ContentFile(resized.read()), True)
    #             # try:
    #             #     delete(temp_header_img_name)
    #             # except: # ここの例外は自身のものに変える
    #             #     pass
    #     if self.icon_image:
    #         if self.icon_image.width > 300 or self.icon_image.height > 300:
    #             resized = get_thumbnail(self.icon_image, "{}x{}".format(new_width, new_height))
    #             # name = resized.name.split('/')[-1]
    #             self.icon_image.save(self.icon_image.name.split('/')[-1], ContentFile(resized.read()), True)
    #             # try:
    #             #     delete(temp_icon_img_name)
    #             # except: # ここの例外は自身のものに変える
    #             #     pass