from django.db import migrations


def transfer_wrong_answers(apps, schema_editor):
    DeckPerformance = apps.get_model('users', 'DeckPerformance')
    ChineseWord = apps.get_model('chineseword', 'ChineseWord')

    for performance in DeckPerformance.objects.all():
        if performance.wrong_answers and performance.wrong_answers != 'None':
            # Split the wrong answers into a list and strip whitespace
            word_list = [word.strip() for word in performance.wrong_answers.split(',') if word.strip()]
            for word in word_list:
                try:
                    # Try to find the word by its content (simplified or traditional)
                    chinese_word = ChineseWord.objects.filter(simplified=word).first() or ChineseWord.objects.filter(
                        traditional=word).first()

                    if chinese_word:
                        # If the word exists, add it to the Many-to-Many field
                        performance.wrong_answers_m2m.add(chinese_word)
                    else:
                        # If the word does not exist, create a new ChineseWord instance
                        new_chinese_word = ChineseWord.objects.create(simplified=word)
                        performance.wrong_answers_m2m.add(new_chinese_word)
                        print(f"Created new word: '{word}'")

                except Exception as e:
                    print(f"Error processing word '{word}': {str(e)}")

            performance.save()



class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_auto_20241012_1735'),
    ]

    operations = [
        migrations.RunPython(transfer_wrong_answers),
    ]