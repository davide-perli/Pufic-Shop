# Generated by Django 4.2.11 on 2024-11-07 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gelaterie', '0006_alter_bauturi_bautura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prajituri',
            name='nume_prajitura',
            field=models.CharField(choices=[('MOUSSE', 'mousse'), ('LAVACAKE', 'lavacke'), ('PROFITEROL', 'profiterol'), ('TARTE FRUCTE', 'tarte fructe'), ('CREME BRULEE', 'creme brulee'), ('ECLAIR', 'eclair'), ('MACAROONS', 'macaroons'), ('RED VELVET', 'red velvet')], default='MOUSSE'),
        ),
    ]
