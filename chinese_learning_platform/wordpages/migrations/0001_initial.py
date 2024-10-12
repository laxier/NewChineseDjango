# Generated by Django 5.1.2 on 2024-10-12 21:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chineseword', '0007_alter_chineseword_simplified_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('chinese_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentences', to='chineseword.chineseword')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_to', to='chineseword.chineseword')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_words', to='chineseword.chineseword')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('word', 'related_word'), name='unique_related_word_pair')],
            },
        ),
    ]