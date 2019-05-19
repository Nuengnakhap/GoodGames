
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from goodgames.models import Player, Team, Match, Tournament, Categories


class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'name',
            'short_name',
            'picture',
            'phone',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Team name'}),
            'short_name': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Team short name'}),
            'picture': forms.FileInput(attrs={'class': 'custom-file-input', 'placeholder': 'Enter Your Team Logo', 'type': 'file'}),
            'phone': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Team Phone'}),
            'description': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Team Descriptions'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Team.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("team name is taken")
        return name

    def clean_short_name(self):
        name = self.cleaned_data['short_name']
        qs = Team.objects.filter(short_name=name)
        if qs.exists():
            raise forms.ValidationError("team short name is taken")
        return name


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
            'firstName': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your First Name'}),
            'lastName': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Last Name'}),
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


class ManageTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'picture',
            'phone',
            'description',
        ]
        widgets = {
            'picture': forms.FileInput(
                attrs={'class': 'custom-file-input', 'placeholder': 'Enter Your Team Logo', 'type': 'file'}),
            'phone': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Team Phone'}),
            'description': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Team Descriptions'}),
        }


class ManagePlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'firstName',
            'lastName',
            'email',
            'phone1',
            'phone2',
            'province',
            'sex',
            'birthday'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Email'}),
            'firstName': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your First Name'}),
            'lastName': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Last Name'}),
            'sex': forms.Select(attrs={'class': 'js-select2'}),
            'birthday': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'phone1': forms.NumberInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Phone'}),
            'phone2': forms.NumberInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Phone'}),
            'province': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Province'}),
        }


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'picture'
        ]
        widgets = {
            'picture': forms.FileInput(attrs={'class': 'custom-file-input', 'placeholder': 'Enter Your EVIDENCE', 'type': 'file'}),
        }


class CreateTournamentForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False, widget=forms.Select(attrs={'class': 'input100'}))

    class Meta:
        model = Tournament
        fields = [
            'name',
            'rule',
            'prize',
            'start_date',
            'end_date',
            'categories',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament name'}),
            'rule': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament rules'}),
            'prize': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament prizes'}),
            'start_date': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament descriptions'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        qs = Tournament.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Tournament name is taken")
        return name

    # def clean_categories(self):
    #     category = self.cleaned_data['categories']
    #     cleaned_data = super().clean()
    #     new_category = cleaned_data.get('new_category')
    #     if category == None:
    #         Categories.objects.create(description=new_category)
    #     return category


class ManageTournamentForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Categories.objects.all(), required=False, widget=forms.Select(attrs={'class': 'input100'}))

    class Meta:
        model = Tournament
        fields = [
            'rule',
            'prize',
            'start_date',
            'end_date',
            'categories',
            'description',
        ]
        widgets = {
            'rule': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament rules'}),
            'prize': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament prizes'}),
            'start_date': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'input100', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'input100', 'placeholder': 'Enter Your Tournament descriptions'}),
        }