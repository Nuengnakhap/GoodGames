# Generated by Django 2.2 on 2019-05-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodgames', '0005_remove_player_password_confirm'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='player',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]