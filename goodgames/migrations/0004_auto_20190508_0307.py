# Generated by Django 2.1.7 on 2019-05-07 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodgames', '0003_auto_20190508_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='picture',
            field=models.FileField(null=True, upload_to='media'),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_away',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_home',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='picture',
            field=models.FileField(null=True, upload_to='media'),
        ),
    ]