# Generated by Django 4.2.5 on 2023-10-14 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
