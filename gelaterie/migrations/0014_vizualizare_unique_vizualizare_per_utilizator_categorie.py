# Generated by Django 4.2.11 on 2024-12-05 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gelaterie', '0013_remove_vizualizare_unique_vizualizare_per_utilizator_categorie'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='vizualizare',
            constraint=models.UniqueConstraint(fields=('utilizator', 'categorie'), name='unique_vizualizare_per_utilizator_categorie'),
        ),
    ]
