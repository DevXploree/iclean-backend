# Generated by Django 4.2.5 on 2023-10-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_users', '0003_remove_installationpersons_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmanagers',
            name='fcm_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
