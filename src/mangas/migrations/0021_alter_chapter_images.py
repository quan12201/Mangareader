# Generated by Django 4.1.3 on 2023-01-04 17:40

from django.db import migrations, models
import mangas.models


class Migration(migrations.Migration):

    dependencies = [
        ("mangas", "0020_alter_chapter_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="images",
            field=models.FileField(upload_to=mangas.models.path_file_name),
        ),
    ]
