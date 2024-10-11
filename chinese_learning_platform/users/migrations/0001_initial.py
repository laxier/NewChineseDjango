from django.db import migrations, models
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # t this line based on your ChineseWord app's initial migration
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creator', models.ForeignKey(on_delete=models.CASCADE, related_name='decks_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDeck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('deck', models.ForeignKey(on_delete=models.CASCADE, to='users.Deck')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'deck')},
            },
        ),
        migrations.CreateModel(
            name='DeckWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('deck', models.ForeignKey(on_delete=models.CASCADE, related_name='deck_words', to='users.Deck')),
                ('word', models.ForeignKey(on_delete=models.CASCADE, related_name='deck_words', to='chineseword.ChineseWord')),
            ],
            options={
                'unique_together': {('deck', 'word')},
            },
        ),
        migrations.CreateModel(
            name='WordPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ef_factor', models.FloatField(default=2)),
                ('repetitions', models.IntegerField(default=0)),
                ('right', models.IntegerField(default=0)),
                ('wrong', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('next_review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=models.CASCADE, related_name='performance', to='chineseword.ChineseWord')),
            ],
            options={
                'unique_together': {('user', 'word')},
            },
        ),
        migrations.CreateModel(
            name='DeckPerformance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percent_correct', models.IntegerField()),
                ('test_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('wrong_answers', models.TextField()),
                ('deck', models.ForeignKey(on_delete=models.CASCADE, to='users.Deck')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'deck')},
            },
        ),
    ]
