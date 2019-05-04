# Generated by Django 2.2 on 2019-05-04 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodgames', '0004_auto_20190504_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizer',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='short_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='prize',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='rule',
            field=models.TextField(),
        ),
    ]
