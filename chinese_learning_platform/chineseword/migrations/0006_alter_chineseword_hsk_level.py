# Generated by Django 5.1.2 on 2024-10-10 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chineseword', '0005_chineseword_hsk_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chineseword',
            name='hsk_level',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
