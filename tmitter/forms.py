from django import forms
from .models import Tmeet, DmMessage
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class TmeetForm(forms.ModelForm):
    class Meta:
        model = Tmeet
        fields = ('content', 'picture1')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('header_image', 'icon_image','nickname', 'description')

class DmForm(forms.ModelForm):
    class Meta:
        model = DmMessage
        fields = ('content', )