# Generated by Django 5.1.2 on 2024-10-10 21:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_deck_users_deck_words_alter_deck_id_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='deckperformance',
            unique_together=set(),
        ),
    ]
