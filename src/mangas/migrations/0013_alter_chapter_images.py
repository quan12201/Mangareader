# Generated by Django 4.1.3 on 2022-12-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mangas", "0012_alter_chapter_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="images",
            field=models.ImageField(upload_to="content/None"),
        ),
    ]