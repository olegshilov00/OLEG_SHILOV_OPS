from django import forms
from .models import News
from captcha.fields import CaptchaField

class NewsForm(forms.ModelForm):
    captcha = CaptchaField(label="Введите текст с картинки")
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'category', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple,
        }
