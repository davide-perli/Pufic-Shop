# Generated by Django 4.2.11 on 2024-12-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gelaterie', '0019_alter_promotie_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotie',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
