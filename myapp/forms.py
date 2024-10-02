from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,Talk
from django.forms import ModelForm, HiddenInput, TextInput
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_icon_image',)

class TalkForm(ModelForm):
    
    class Meta:
        model = Talk
        fields = ("sender","receiver", "content",)
        widgets = {
                    "sender": HiddenInput,
                    "receiver": HiddenInput,
                    "content": TextInput,
                   }
