# Generated by Django 2.1.7 on 2019-05-08 01:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodgames', '0004_auto_20190508_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='team_create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='team_create', to='goodgames.Team'),
        ),
    ]
