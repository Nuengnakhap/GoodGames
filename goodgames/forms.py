from django.contrib.auth.forms import UserCreationForm

from goodgames.models import Player, Team


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Player
        exclude = ['team', 'last_login', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password_confirm")
        if password1 and password2 and password1 != password2:
            self.add_error('tel', "ต้องกรอก email หรือ Mobile Number")

    def save(self, commit=True):
        cleaned_data = super().clean()

        user = super(RegistrationForm, self).save(commit=False)
        user.username = cleaned_data.get('username')
        user.set_password(cleaned_data.get('password'))
        user.firstName = cleaned_data.get('firstName')
        user.lastName = cleaned_data.get('lastName')
        user.email = cleaned_data.get('email')
        user.type = cleaned_data.get('type')
        user.birthday = cleaned_data.get('birthday')
        user.phone1 = cleaned_data.get('phone1')
        user.phone2 = cleaned_data.get('phone2')
        user.province = cleaned_data.get('province')
        user.team = Team.objects.get(id='1')

        if commit:
            user.save()

        return user

