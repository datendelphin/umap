# Generated by Django 4.2.2 on 2023-10-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("umap", "0015_alter_pictogram_pictogram"),
    ]

    operations = [
        migrations.AddField(
            model_name="pictogram",
            name="category",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
