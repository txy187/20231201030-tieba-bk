from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '介绍一下你自己...',
                'rows': 4
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入所在地'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入个人网站地址'
            }),
        }