from django.db import migrations


def transfer_wrong_answers(apps, schema_editor):
    DeckPerformance = apps.get_model('users', 'DeckPerformance')
    ChineseWord = apps.get_model('chineseword', 'ChineseWord')

    for performance in DeckPerformance.objects.all():
        if performance.wrong_answers:
            word_list = [word.strip() for word in performance.wrong_answers.split(',') if word.strip()]
            for word in word_list:
                try:
                    # Try to find the word by its content (simplified or traditional)
                    chinese_word = ChineseWord.objects.filter(simplified=word).first()
                    if chinese_word:
                        performance.wrong_answers_m2m.add(chinese_word)
                    else:
                        print(f"Warning: Word '{word}' not found in ChineseWord model.")
                except Exception as e:
                    print(f"Error processing word '{word}': {str(e)}")

            performance.save()



class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_deckperformance_wrong_answers_m2m'),
    ]

    operations = [
        migrations.RunPython(transfer_wrong_answers),
    ]
