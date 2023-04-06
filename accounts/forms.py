from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser, CustomerPhoto


# This is a custom form for creating new users in the admin interface.
# It inherits from the built-in UserCreationForm and adds custom fields if necessary.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email", )

# This is a custom form for editing existing users in the admin interface.
# It inherits from the built-in UserChangeForm and adds custom fields if necessary.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", )

# This is a custom form for adding/editing customer photos in the admin interface.
# It inherits from the built-in ModelForm and adds custom fields if necessary.
class CustomerPhotoForm(forms.ModelForm):
    class Meta:
        model = CustomerPhoto
        fields = ( "photo", )