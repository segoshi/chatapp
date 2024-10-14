from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.user_icon_image = form.cleaned_data.get("user_icon_image")
        if commit:
            user.save()
        return user