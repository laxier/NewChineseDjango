# Generated by Django 5.1.2 on 2024-10-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_deckperformance_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deckperformance',
            name='wrong_answers',
            field=models.TextField(blank=True, default='None'),
        ),
    ]
