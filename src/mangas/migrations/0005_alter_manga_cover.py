# Generated by Django 4.1.3 on 2022-12-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mangas", "0004_alter_manga_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manga",
            name="cover",
            field=models.ImageField(upload_to="cover"),
        ),
    ]
