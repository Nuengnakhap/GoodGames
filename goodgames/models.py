from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


# Create your models here.
SEX = (
        ('01', 'Male'),
        ('02', 'Female')
    )


class Organizer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=SEX, default='01')
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Categories(models.Model):
    description = models.TextField()

    def __str__(self):
        return self.description


class Tournament(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rule = models.TextField()
    prize = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    categories = models.ForeignKey(Categories, on_delete=models.PROTECT)
    organizer = models.ForeignKey(Organizer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=100, unique=True)
    picture = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    score_home = models.CharField(max_length=100)
    score_away = models.CharField(max_length=100)
    team = models.ManyToManyField(Team, related_name='matchs')
    start_date = models.DateField()
    end_date = models.DateField()
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)
    winner = models.ForeignKey(Team, null=True, on_delete=models.PROTECT, related_name='match_winner')
    loser = models.ForeignKey(Team, null=True, on_delete=models.PROTECT, related_name='match_loser')

    def get_teams(self):
        return " VS ".join([p.name for p in self.team.all()])


class Appointment(models.Model):
    team = models.ManyToManyField(Team)
    start_date = models.DateField()
    end_date = models.DateField()

    def get_teams(self):
        return "\n".join([p.name for p in self.team.all()])


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not password:
            raise ValueError('Users must have an password')
        user = self.model(
            username=self.normalize_username(username),
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            is_staff=True
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password,
            is_admin=True
        )
        user.save(using=self._db)
        return user


class Player(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    sex = models.CharField(max_length=2, choices=SEX, default='01')
    birthday = models.DateField(null=True)
    phone1 = models.CharField(max_length=10, null=True)
    phone2 = models.CharField(max_length=10, null=True)
    province = models.CharField(max_length=100, null=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.firstName + " " + self.lastName

    def get_short_name(self):
        return self.firstName

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active



