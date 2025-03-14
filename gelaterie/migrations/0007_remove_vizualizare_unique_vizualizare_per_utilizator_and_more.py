# Generated by Django 4.2.11 on 2024-12-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gelaterie', '0006_remove_vizualizare_categorie'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='vizualizare',
            name='unique_vizualizare_per_utilizator',
        ),
        migrations.RemoveField(
            model_name='vizualizare',
            name='produs',
        ),
        migrations.AddField(
            model_name='vizualizare',
            name='produs_nume',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='vizualizare',
            name='produs_pret',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='vizualizare',
            name='produs_tip',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddConstraint(
            model_name='vizualizare',
            constraint=models.UniqueConstraint(fields=('utilizator', 'produs_nume'), name='unique_vizualizare_per_utilizator'),
        ),
    ]
