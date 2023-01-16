from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Tmeet(models.Model):
    content = models.TextField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    like = models.ManyToManyField(CustomUser, related_name='related_post', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picture1 = models.ImageField(null=True, blank=True, upload_to='picture')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child', null=True, blank=True)

    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['-created_at']

class Connection(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.follower.username, self.following.username)

class Notification(models.Model):
    # 各種類の通知のfieldについて
    # followed: kind, user, by_user
    # liked:    kind, user, by_user, tmeet
    # reply:    kind, user, tmeet,   by_tmeet

    # 共通
    kind = models.IntegerField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notification')
    created_at = models.DateTimeField(auto_now_add=True)
    be_read = models.BooleanField(default=False)
    pre_be_read = models.BooleanField(default=False)

    # followedとliked
    by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_notification', null=True, blank=True)
    # replyとliked
    tmeet = models.ForeignKey(Tmeet, on_delete=models.CASCADE, related_name='tmeet', null=True, blank=True)
    # reply
    by_tmeet = models.ForeignKey(Tmeet, on_delete=models.CASCADE, related_name='to_tmeet', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class DmRoom(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='dm_rooms')
    last_updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    # be_read = models.BooleanField(default=False)
    has_read_users = models.ManyToManyField(CustomUser)

    class Meta:
        ordering = ['-last_updated_at']

class DmMessage(models.Model):
    dm_room = models.ForeignKey(DmRoom, on_delete=models.CASCADE, related_name='dm_room')
    # dmの作成者
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']