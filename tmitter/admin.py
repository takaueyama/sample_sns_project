from django.contrib import admin
from .models import Tmeet, Connection, Notification, DmRoom, DmMessage


admin.site.register(Tmeet)
admin.site.register(Connection)
admin.site.register(Notification)
admin.site.register(DmRoom)
admin.site.register(DmMessage)