# Generated by Django 4.1.3 on 2023-02-16 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mangas", "0029_alter_volume_timestamp"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="volume",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="mangas.volume",
            ),
        ),
    ]
