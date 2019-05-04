from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models


# Create your models here.
SEX = (
        ('01', 'male'),
        ('02', 'female')
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

    def __str__(self):
        return self.name


class Match(models.Model):
    score_home = models.CharField(max_length=100)
    score_away = models.CharField(max_length=100)
    team = models.ManyToManyField(Team)
    start_date = models.DateField()
    end_date = models.DateField()
    tournament = models.ForeignKey(Tournament, on_delete=models.PROTECT)

    def get_teams(self):
        return "\n".join([p.name for p in self.team.all()])



class Appointment(models.Model):
    team = models.ManyToManyField(Team)
    start_date = models.DateField()
    end_date = models.DateField()

    def get_teams(self):
        return "\n".join([p.name for p in self.team.all()])


class Player(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    sex = models.CharField(max_length=2, choices=SEX, default='01')
    birthday = models.DateField(default='1999-01-01')
    phone1 = models.CharField(max_length=10, default='0000000000')
    phone2 = models.CharField(max_length=10, default='0000000000')
    province = models.CharField(max_length=100, default='Bangkok')
    team = models.ForeignKey(Team, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.firstName + " " + self.lastName

    def get_short_name(self):
        return self.firstName

    def date_joined(self):
        return self.created_at


