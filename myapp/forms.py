from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Talk
from django import forms
from django.forms import ModelForm, HiddenInput, TextInput
from allauth.account.forms import SignupForm



class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_icon_image',)

class TalkForm(ModelForm):
    
    class Meta:
        # sender, receiverはビューで決める
        model = Talk
        fields = ("content",)
        widgets = {
                    "content": TextInput,
                   }

class CustomSignupForm(SignupForm):
    user_icon_image = forms.ImageField(required=False, label="アイコン画像")
    
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.user_icon_image = self.cleaned_data.get("user_icon_image")
        user.save()
        return user

