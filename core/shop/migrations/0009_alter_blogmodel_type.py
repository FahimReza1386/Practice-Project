# Generated by Django 5.2.4 on 2025-07-18 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_categorymodel_blogcategorymodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='type',
            field=models.IntegerField(choices=[(1, 'Premium'), (2, 'Normal')], default=2),
        ),
    ]
