# Generated by Django 3.1.6 on 2021-05-08 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_favourites_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='favourites',
            name='mpg',
            field=models.FloatField(default='55.5'),
            preserve_default=False,
        ),
    ]
