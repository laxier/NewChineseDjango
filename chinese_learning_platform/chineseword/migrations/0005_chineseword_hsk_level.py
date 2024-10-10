# Generated by Django 5.1.2 on 2024-10-10 17:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chineseword', '0004_alter_chineseword_meaning_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chineseword',
            name='hsk_level',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
