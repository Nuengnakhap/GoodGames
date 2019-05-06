
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms

from goodgames.models import Player, Team


class RegistrationForm(forms.ModelForm):
    pass_field = forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Password', 'type': 'password'})
    password1 = forms.CharField(widget=pass_field)
    password2 = forms.CharField(widget=pass_field)

    class Meta:
        model = Player
        fields = [
            'username',
            'email',
            'firstName',
            'lastName',
            'sex',
            'birthday',
            'phone1',
            'phone2',
            'province',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Username'}),
            'email': forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Email'}),
            'firstName': forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Enter Your First Name'}),
            'lastName': forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Last Name'}),
            'sex': forms.Select(attrs={'class': 'js-select2'}),
            'birthday': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'phone1': forms.NumberInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Phone'}),
            'phone2': forms.NumberInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Phone'}),
            'province': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Province'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = Player.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("username is taken")
        return username

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Player
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Player
        fields = ('username', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]