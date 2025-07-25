# Generated by Django 5.2.4 on 2025-07-18 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_blogmodel_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CategoryModel',
            new_name='BlogCategoryModel',
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='image',
            field=models.ImageField(default='blogs/image.jpg', upload_to='blogs/'),
        ),
    ]
