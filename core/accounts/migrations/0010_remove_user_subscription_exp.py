# Generated by Django 5.2.4 on 2025-07-18 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_rename_subscriptionmodel_usersubscriptionmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscription_exp',
        ),
    ]
