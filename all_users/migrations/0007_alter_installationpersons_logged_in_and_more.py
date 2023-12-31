# Generated by Django 4.2.5 on 2023-10-22 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all_users', '0006_installationpersons_logged_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installationpersons',
            name='logged_in',
            field=models.CharField(default='installation_person', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='projectmanagers',
            name='logged_in',
            field=models.CharField(default='project_manager', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='salespersons',
            name='logged_in',
            field=models.CharField(default='sales_person', editable=False, max_length=50),
        ),
    ]
