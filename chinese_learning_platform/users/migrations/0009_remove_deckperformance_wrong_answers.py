# Generated by Django 5.1.2 on 2024-10-12 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20241012_1737'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deckperformance',
            name='wrong_answers',
        ),
    ]
